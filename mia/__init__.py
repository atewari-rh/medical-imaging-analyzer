"""
Medical Imaging Analyzer - Core Package
An open-source privacy-first medical image analysis tool
"""

__version__ = "0.1.0"
__author__ = "Medical Imaging Analyzer Contributors"
__license__ = "Apache License 2.0"

from .core.analyzer import ImageAnalyzer
from .core.model_loader import ModelLoader

__all__ = ["ImageAnalyzer", "ModelLoader", "__version__"]
