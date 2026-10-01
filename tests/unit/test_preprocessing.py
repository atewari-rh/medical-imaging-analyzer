"""
Test preprocessing module
"""

import pytest
from PIL import Image
import numpy as np

from mia.core.preprocessing import ImagePreprocessor


@pytest.fixture
def preprocessor():
    """Create preprocessor instance"""
    return ImagePreprocessor(target_size=(256, 256))


@pytest.fixture
def sample_image():
    """Create a sample image"""
    return Image.new('L', (512, 512), color=128)


def test_preprocessor_init(preprocessor):
    """Test preprocessor initialization"""
    assert preprocessor.target_size == (256, 256)
    assert preprocessor.normalize == True


def test_resize_image(preprocessor, sample_image):
    """Test image resizing"""
    resized = preprocessor._resize_image(sample_image)
    assert resized.size == (256, 256)


def test_process_image(preprocessor, sample_image):
    """Test full preprocessing pipeline"""
    result = preprocessor.process(sample_image)
    
    assert isinstance(result, np.ndarray)
    assert result.shape == (256, 256)
    assert result.dtype == np.float32


def test_normalize(preprocessor):
    """Test image normalization"""
    test_array = np.array([[0, 128, 255]], dtype=np.float32)
    normalized = preprocessor._normalize(test_array)
    
    assert normalized.max() <= 1.0
    assert normalized.min() >= 0.0


def test_enhance_contrast(preprocessor, sample_image):
    """Test contrast enhancement"""
    enhanced = preprocessor._enhance_contrast(sample_image)
    assert enhanced.size == sample_image.size
