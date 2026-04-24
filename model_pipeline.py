import torch
from transformers import pipeline
from PIL import Image

class FoodDetector:
    def __init__(self):
        # We use a general image classification model fine-tuned on food-101.
        # "nateraw/food" is a popular choice on HuggingFace for this dataset.
        self.model_name = "nateraw/food"
        print(f"Loading image classification model {self.model_name}...")
        self.classifier = pipeline("image-classification", model=self.model_name)
        print("Model loaded.")

    def detect_food(self, image_path_or_pil):
        if isinstance(image_path_or_pil, str):
            image = Image.open(image_path_or_pil)
        else:
            image = image_path_or_pil
            
        # Ensure image is RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Returns a list of dicts: [{'score': 0.9, 'label': 'pizza'}, ...]
        results = self.classifier(image)
        return results
