"""
Image preprocessing module
"""

import logging
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from typing import Tuple

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """Handles medical image preprocessing"""
    
    def __init__(
        self,
        target_size: Tuple[int, int] = (256, 256),
        normalize: bool = True
    ):
        """
        Initialize preprocessor
        
        Args:
            target_size: Target image size for model input
            normalize: Whether to normalize pixel values
        """
        self.target_size = target_size
        self.normalize = normalize
    
    def process(self, image: Image.Image) -> np.ndarray:
        """
        Apply full preprocessing pipeline
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed numpy array
        """
        # Resize
        image = self._resize_image(image)
        
        # Apply contrast enhancement for better visibility
        image = self._enhance_contrast(image)
        
        # Convert to numpy array
        image_array = np.array(image, dtype=np.float32)
        
        # Normalize
        if self.normalize:
            image_array = self._normalize(image_array)
        
        return image_array
    
    def _resize_image(self, image: Image.Image) -> Image.Image:
        """Resize image to target size"""
        # Preserve aspect ratio by using thumbnail and padding
        image.thumbnail(self.target_size, Image.Resampling.LANCZOS)
        
        # Pad to exact size if needed
        if image.size != self.target_size:
            # Calculate padding
            delta_w = self.target_size[0] - image.size[0]
            delta_h = self.target_size[1] - image.size[1]
            
            # Pad with zeros (black)
            image = ImageOps.expand(
                image,
                border=(delta_w // 2, delta_h // 2,
                       delta_w - delta_w // 2, delta_h - delta_h // 2),
                fill=0
            )
        
        return image
    
    def _enhance_contrast(self, image: Image.Image) -> Image.Image:
        """Enhance contrast for better analysis"""
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        return image
    
    def _normalize(self, image_array: np.ndarray) -> np.ndarray:
        """Normalize image values to [0, 1]"""
        max_val = image_array.max()
        if max_val > 0:
            image_array = image_array / max_val
        return image_array
    
    def preprocess_batch(
        self,
        images: list
    ) -> np.ndarray:
        """
        Preprocess multiple images
        
        Args:
            images: List of PIL Images
            
        Returns:
            Stacked preprocessed array
        """
        processed = [self.process(img) for img in images]
        return np.stack(processed)
