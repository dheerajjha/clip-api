from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import time

from app.model import CLIPModel

app = FastAPI(
    title="CLIP API",
    description="API for OpenAI's CLIP model for image-text similarity",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model
clip_model = None

@app.on_event("startup")
async def startup_event():
    global clip_model
    clip_model = CLIPModel()

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    text: str = Form(...)
):
    if not clip_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        image_data = await image.read()
        similarity = clip_model.calculate_similarity(image_data, text)
        return {
            "similarity": similarity,
            "text": text,
            "image_filename": image.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/encode_image")
async def encode_image(image: UploadFile = File(...)):
    if not clip_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        image_data = await image.read()
        features = clip_model.encode_image(image_data)
        return {"features": features, "image_filename": image.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error encoding image: {str(e)}")

@app.post("/encode_text")
async def encode_text(text: str = Form(...)):
    if not clip_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        features = clip_model.encode_text(text)
        return {"features": features, "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error encoding text: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)
