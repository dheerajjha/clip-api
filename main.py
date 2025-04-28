import clip
import torch
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI(
    title="CLIP API",
    description="API for OpenAI's CLIP model to compute image-text similarity",
    version="1.0.0"
)

# Global variables for model and device
# Always use CPU as specified by the user
device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
model.eval()  # Set the model to evaluation mode

def preprocess_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return preprocess(image).unsqueeze(0).to(device)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

def encode_text(text):
    try:
        text_tokens = clip.tokenize([text]).to(device)
        with torch.no_grad():
            text_features = model.encode_text(text_tokens)
        return text_features.float()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing text: {str(e)}")

def encode_image(image):
    try:
        with torch.no_grad():
            image_features = model.encode_image(image)
        return image_features.float()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.post("/predict/")
async def predict(file: UploadFile = File(...), text: str = ""):
    """
    Compute similarity between an image and text using CLIP model.
    
    Parameters:
    - file: Image file to analyze
    - text: Text to compare with the image
    
    Returns:
    - similarity: Cosine similarity score between image and text embeddings
    """
    if not text:
        raise HTTPException(status_code=400, detail="Text query is required")
    
    # Read and preprocess the image
    image_bytes = await file.read()
    image = preprocess_image(image_bytes)
    
    # Generate embeddings
    image_features = encode_image(image)
    text_features = encode_text(text)
    
    # Normalize features
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    
    # Compute similarity
    similarity = torch.cosine_similarity(image_features, text_features)
    
    return JSONResponse(content={
        "similarity": float(similarity[0]),
        "text": text,
        "filename": file.filename
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": "CLIP ViT-B/32", "device": device}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
