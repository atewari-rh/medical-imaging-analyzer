"""
Test model loader module
"""

import pytest
from mia.core.model_loader import ModelLoader, ChestXrayModel


@pytest.fixture
def loader():
    """Create model loader instance"""
    return ModelLoader()


def test_loader_init(loader):
    """Test loader initialization"""
    assert loader is not None
    assert loader.loaded_models == {}


def test_get_available_models(loader):
    """Test getting available models"""
    models = loader.get_available_models()
    assert isinstance(models, list)
    assert len(models) > 0
    assert "chest-xray" in models
    assert "ct-lung" in models


def test_get_model_info(loader):
    """Test getting model information"""
    info = loader.get_model_info("chest-xray")
    
    assert "description" in info
    assert "accuracy" in info
    assert "status" in info
    assert "supported_formats" in info


def test_load_model(loader):
    """Test loading a model"""
    model = loader.load_model("chest-xray")
    assert model is not None
    assert model.name == "chest-xray"


def test_load_model_caching(loader):
    """Test that models are cached"""
    model1 = loader.load_model("chest-xray")
    model2 = loader.load_model("chest-xray")
    assert model1 is model2


def test_load_unknown_model(loader):
    """Test loading unknown model raises error"""
    with pytest.raises(ValueError):
        loader.load_model("unknown-model")


def test_chest_xray_model():
    """Test chest X-ray model"""
    model = ChestXrayModel()
    
    assert model.name == "chest-xray"
    assert model.model_type == "chest_xray"
    
    # Test prediction (dummy)
    import numpy as np
    dummy_image = np.random.rand(256, 256)
    predictions = model.predict(dummy_image)
    
    assert "predictions" in predictions
    assert "confidence" in predictions
