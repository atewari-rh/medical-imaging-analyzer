"""
Integration tests
"""

import pytest
import tempfile
from pathlib import Path
from PIL import Image

from mia.core import ImageAnalyzer


@pytest.fixture
def test_images_dir():
    """Create temporary directory with test images"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create 3 test images
        for i in range(3):
            img = Image.new('L', (256, 256), color=100 + i*20)
            img.save(Path(tmpdir) / f"test_image_{i}.png")
        yield tmpdir


def test_batch_analysis(test_images_dir):
    """Test batch image analysis"""
    analyzer = ImageAnalyzer()
    results = analyzer.batch_analyze(test_images_dir, "chest-xray")
    
    assert len(results) == 3
    for result in results:
        assert result.model_name == "chest-xray"
        assert result.processing_time > 0


def test_batch_analysis_with_output(test_images_dir):
    """Test batch analysis with output file"""
    analyzer = ImageAnalyzer()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "results.json"
        results = analyzer.batch_analyze(
            test_images_dir,
            "chest-xray",
            output_file=str(output_file)
        )
        
        assert output_file.exists()
        assert len(results) == 3
