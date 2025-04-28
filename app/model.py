import torch
import clip
from PIL import Image
import io

class CLIPModel:
    def __init__(self):
        # Always use CPU as specified by the user
        self.device = "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        print(f"Model loaded on {self.device}")

    def encode_image(self, image_data):
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
        return image_features.cpu().numpy().tolist()[0]

    def encode_text(self, text):
        text_input = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
        return text_features.cpu().numpy().tolist()[0]

    def calculate_similarity(self, image_data, text):
        image_features = torch.tensor(self.encode_image(image_data)).to(self.device)
        text_features = torch.tensor(self.encode_text(text)).to(self.device)
        
        # Normalize features
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        # Calculate similarity (using permute to avoid deprecation warning)
        similarity = (100.0 * (image_features @ text_features)).item()
        return similarity
