"""
Custom model example - Create and register a custom model
"""

from mia.core.model_loader import BaseModel
import numpy as np

class CustomModel(BaseModel):
    """Example custom model for demonstration"""
    
    def __init__(self):
        super().__init__("custom-model", "custom")
    
    def predict(self, image: np.ndarray):
        """Custom prediction logic"""
        return {
            "predictions": {
                "custom_output": "demo"
            },
            "confidence": {
                "score": 0.5
            }
        }

# To use this model:
# 1. Create a model instance
# model = CustomModel()
# 2. Register it in ModelLoader.MODEL_REGISTRY
# 3. Use it with analyzer.analyze(image_path, "custom-model")
