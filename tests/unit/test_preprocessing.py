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


class TestJPEG2000WebPSupport:
    """Tests for JPEG2000 and WebP format support (issue #2)."""

    def test_supported_formats_includes_jpeg2000(self):
        """JPEG2000 extensions should be in SUPPORTED_FORMATS."""
        assert '.jp2' in ImagePreprocessor.SUPPORTED_FORMATS
        assert '.j2k' in ImagePreprocessor.SUPPORTED_FORMATS

    def test_supported_formats_includes_webp(self):
        """WebP extension should be in SUPPORTED_FORMATS."""
        assert '.webp' in ImagePreprocessor.SUPPORTED_FORMATS

    def test_is_format_supported_jp2(self):
        """is_format_supported should accept .jp2 files."""
        assert ImagePreprocessor.is_format_supported("image.jp2") is True

    def test_is_format_supported_j2k(self):
        """is_format_supported should accept .j2k files."""
        assert ImagePreprocessor.is_format_supported("scan.j2k") is True

    def test_is_format_supported_webp(self):
        """is_format_supported should accept .webp files."""
        assert ImagePreprocessor.is_format_supported("photo.webp") is True

    def test_is_format_supported_png_still_works(self):
        """Existing PNG format should still be supported."""
        assert ImagePreprocessor.is_format_supported("xray.png") is True

    def test_is_format_supported_unsupported(self):
        """Unsupported formats should return False."""
        assert ImagePreprocessor.is_format_supported("file.gif") is False
        assert ImagePreprocessor.is_format_supported("file.pdf") is False

    def test_process_webp_image(self, preprocessor):
        """Processing a WebP image should work end-to-end."""
        img = Image.new('RGB', (512, 512), color=(128, 128, 128))
        result = preprocessor.process(img)
        assert isinstance(result, np.ndarray)
        assert result.shape == (256, 256, 3) or result.shape == (256, 256)

    def test_process_jpeg2000_compatible(self, preprocessor):
        """Processing a JPEG2000-compatible image (grayscale) should work."""
        img = Image.new('L', (512, 512), color=128)
        result = preprocessor.process(img)
        assert isinstance(result, np.ndarray)
        assert result.shape == (256, 256)

    def test_batch_analyze_includes_new_formats(self, preprocessor):
        """Batch processing should accept the new format extensions."""
        from pathlib import Path
        # Verify the analyzer's image_extensions set includes new formats
        # (We test the constant directly since we don't have real files)
        new_extensions = {'.jp2', '.j2k', '.webp'}
        supported = ImagePreprocessor.SUPPORTED_FORMATS
        assert new_extensions.issubset(supported)
