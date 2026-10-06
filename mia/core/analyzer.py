"""
Core analyzer module - Main analysis engine for medical images
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import numpy as np
from PIL import Image

from .preprocessing import ImagePreprocessor
from .model_loader import ModelLoader

logger = logging.getLogger(__name__)


class AnalysisResult:
    """Container for analysis results"""
    
    def __init__(self, image_path: str, model_name: str):
        self.image_path = image_path
        self.model_name = model_name
        self.predictions = {}
        self.confidence_scores = {}
        self.processing_time = 0.0
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "image_path": str(self.image_path),
            "model": self.model_name,
            "predictions": self.predictions,
            "confidence_scores": self.confidence_scores,
            "processing_time": self.processing_time,
            "metadata": self.metadata
        }
    
    def to_json_string(self) -> str:
        """Convert result to JSON string"""
        import json
        return json.dumps(self.to_dict(), indent=2)


class ImageAnalyzer:
    """Main image analyzer class"""
    
    def __init__(self, model_dir: Optional[str] = None):
        """
        Initialize the analyzer
        
        Args:
            model_dir: Directory containing pre-trained models
        """
        self.model_loader = ModelLoader(model_dir)
        self.preprocessor = ImagePreprocessor()
        self.loaded_models = {}
    
    def load_model(self, model_name: str) -> bool:
        """
        Load a model for analysis
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            True if model loaded successfully
        """
        try:
            if model_name not in self.loaded_models:
                model = self.model_loader.load_model(model_name)
                self.loaded_models[model_name] = model
                logger.info(f"Model {model_name} loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            return False
    
    def analyze(
        self,
        image_path: str,
        model_name: str,
        preprocessing: bool = True
    ) -> AnalysisResult:
        """
        Analyze a medical image
        
        Args:
            image_path: Path to the medical image
            model_name: Name of the model to use
            preprocessing: Whether to apply preprocessing
            
        Returns:
            AnalysisResult object with predictions
        """
        import time
        start_time = time.time()
        
        result = AnalysisResult(image_path, model_name)
        
        try:
            # Load model if not already loaded
            if model_name not in self.loaded_models:
                self.load_model(model_name)
            
            # Load and validate image
            image = Image.open(image_path).convert('L')  # Convert to grayscale
            
            # Preprocess image
            if preprocessing:
                processed_image = self.preprocessor.process(image)
            else:
                processed_image = np.array(image)
            
            # Get model and run prediction
            model = self.loaded_models[model_name]
            predictions = model.predict(processed_image)
            
            result.predictions = predictions.get("predictions", {})
            result.confidence_scores = predictions.get("confidence", {})
            result.metadata = {
                "image_size": image.size,
                "preprocessing_applied": preprocessing
            }
            
            result.processing_time = time.time() - start_time
            logger.info(f"Analysis completed in {result.processing_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            result.predictions = {"error": str(e)}
        
        return result
    
    def batch_analyze(
        self,
        image_dir: str,
        model_name: str,
        output_file: Optional[str] = None
    ) -> List[AnalysisResult]:
        """
        Analyze multiple images
        
        Args:
            image_dir: Directory containing images
            model_name: Model to use
            output_file: Optional file to save results
            
        Returns:
            List of AnalysisResult objects
        """
        image_path = Path(image_dir)
        results = []
        
        # Supported image formats
        image_extensions = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.jp2', '.j2k', '.webp'}
        
        for image_file in image_path.iterdir():
            if image_file.suffix.lower() in image_extensions:
                logger.info(f"Processing {image_file.name}...")
                result = self.analyze(str(image_file), model_name)
                results.append(result)
        
        # Save results if output file specified
        if output_file:
            self._save_results(results, output_file)
        
        return results
    
    def _save_results(
        self,
        results: List[AnalysisResult],
        output_file: str
    ) -> None:
        """Save analysis results to file"""
        import json
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results_data = [r.to_dict() for r in results]
        
        with open(output_path, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return self.model_loader.get_available_models()
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a model"""
        return self.model_loader.get_model_info(model_name)
