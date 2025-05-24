import numpy as np
from PIL import Image
from .model import load_model
from .data_preprocessing import preprocess_image
from .config import MODEL_PATH

class HandwritingPredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = MODEL_PATH
        self.model = load_model(model_path)
        print(f"Model loaded from {model_path}")
    
    def predict(self, image):
        if isinstance(image, str):
            image = Image.open(image)
        
        processed = preprocess_image(image)
        processed = np.expand_dims(processed, axis=0)
        
        predictions = self.model.predict(processed, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {"digit": int(idx), "confidence": float(predictions[0][idx])}
            for idx in top_3_indices
        ]
        
        return {
            "predicted_digit": int(predicted_class),
            "confidence": confidence,
            "top_3": top_3_predictions
        }
    
    def predict_batch(self, images):
        return [self.predict(img) for img in images]
