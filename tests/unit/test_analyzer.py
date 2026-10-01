"""
Test analyzer module
"""

import pytest
from pathlib import Path
from PIL import Image
import numpy as np

from mia.core import ImageAnalyzer


@pytest.fixture
def analyzer():
    """Create analyzer instance"""
    return ImageAnalyzer()


@pytest.fixture
def sample_image_path(tmp_path):
    """Create a sample test image"""
    img = Image.new('L', (256, 256), color=128)
    img_path = tmp_path / "test_image.png"
    img.save(img_path)
    return str(img_path)


def test_analyzer_init(analyzer):
    """Test analyzer initialization"""
    assert analyzer is not None
    assert analyzer.loaded_models == {}


def test_get_available_models(analyzer):
    """Test getting available models"""
    models = analyzer.get_available_models()
    assert len(models) > 0
    assert "chest-xray" in models


def test_get_model_info(analyzer):
    """Test getting model information"""
    info = analyzer.get_model_info("chest-xray")
    assert "description" in info
    assert "accuracy" in info
    assert "status" in info


def test_load_model(analyzer):
    """Test loading a model"""
    result = analyzer.load_model("chest-xray")
    assert result == True
    assert "chest-xray" in analyzer.loaded_models


def test_analyze_single_image(analyzer, sample_image_path):
    """Test analyzing a single image"""
    result = analyzer.analyze(sample_image_path, "chest-xray")
    
    assert result is not None
    assert result.image_path == sample_image_path
    assert result.model_name == "chest-xray"
    assert "predictions" in result.__dict__
    assert result.processing_time > 0


def test_analyze_result_to_dict(analyzer, sample_image_path):
    """Test converting analysis result to dict"""
    result = analyzer.analyze(sample_image_path, "chest-xray")
    result_dict = result.to_dict()
    
    assert isinstance(result_dict, dict)
    assert "image_path" in result_dict
    assert "model" in result_dict
    assert "predictions" in result_dict


def test_analyze_result_to_json(analyzer, sample_image_path):
    """Test converting analysis result to JSON"""
    result = analyzer.analyze(sample_image_path, "chest-xray")
    json_str = result.to_json_string()
    
    assert isinstance(json_str, str)
    assert "image_path" in json_str
    assert "predictions" in json_str
