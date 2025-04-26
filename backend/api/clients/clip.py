import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from api.config import Settings


class CLIPClient:
    def __init__(self, settings: Settings):
        self.clip_model = CLIPModel.from_pretrained(settings.CLIP_EMBEDDING_MODEL).to(
            settings.DEVICE
        )
        self.clip_processor = CLIPProcessor.from_pretrained(
            settings.CLIP_EMBEDDING_MODEL
        )

    def generate_image_embedding(self, image: Image.Image) -> np.ndarray:
        """画像の埋め込みベクトルを生成"""
        with torch.no_grad():
            inputs = self.clip_processor(images=image, return_tensors="pt").to(
                self.clip_model.device
            )
            outputs = self.clip_model.get_image_features(**inputs)
            image_embedding = outputs.cpu().numpy()
            return image_embedding[0] / np.linalg.norm(image_embedding[0])

    def generate_text_embedding(self, text: str) -> np.ndarray:
        """テキストの埋め込みベクトルを生成"""
        with torch.no_grad():
            inputs = self.clip_processor(
                text=[text], return_tensors="pt", padding=True, truncation=True
            ).to(self.clip_model.device)
            outputs = self.clip_model.get_text_features(**inputs)
            text_embedding = outputs.cpu().numpy()
            return text_embedding[0] / np.linalg.norm(text_embedding[0])
