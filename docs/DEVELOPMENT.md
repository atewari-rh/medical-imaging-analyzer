# Development Guide

## Getting Started with Development

### Prerequisites
- Python 3.9+
- Git
- ~2GB disk space
- Basic understanding of medical imaging concepts (helpful but not required)

### Initial Setup

```bash
# Clone repository
git clone https://github.com/medical-imaging-analyzer/mia.git
cd mia

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e ".[dev]"
```

## Project Structure

```
mia/
├── core/              # Core analysis engine
│   ├── analyzer.py    # Main analysis class
│   ├── model_loader.py # Model management
│   └── preprocessing.py # Image preprocessing
├── cli.py             # Command-line interface
└── __init__.py        # Package init

tests/
├── unit/              # Unit tests
├── integration/       # Integration tests
└── fixtures/          # Test data

examples/              # Example scripts
docs/                  # Documentation
```

## Common Development Tasks

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=mia

# Run specific test file
pytest tests/unit/test_analyzer.py -v

# Run specific test
pytest tests/unit/test_analyzer.py::test_analyze -v
```

### Code Quality

```bash
# Format code
black mia tests examples

# Check style
flake8 mia tests

# Type checking
mypy mia

# All checks at once
black mia tests && flake8 mia tests && mypy mia
```

### Building Documentation

```bash
cd docs
make html
# Open _build/html/index.html
```

### Installing from Source

```bash
# Install in development mode (editable)
pip install -e .

# Now you can use mia command
mia analyze --image test.png
```

## Adding a New Feature

### 1. Create Feature Branch
```bash
git checkout -b feature/description
```

### 2. Implement Feature
- Add code to appropriate module
- Write comprehensive docstrings
- Include type hints

### 3. Write Tests
```python
# In tests/unit/test_new_feature.py
def test_feature_basic():
    """Test basic functionality"""
    assert True
```

### 4. Update Documentation
- Add to appropriate docs file
- Update README if user-facing
- Include examples

### 5. Commit and Push
```bash
git add .
git commit -m "Feature: Add new capability"
git push origin feature/description
```

### 6. Create Pull Request
- Link related issues
- Describe changes clearly
- Request review

## Architecture Deep Dive

### Image Analysis Pipeline

```
Input Image
    ↓
Validation (format, size)
    ↓
Preprocessing (resize, normalize, enhance)
    ↓
Model Loading
    ↓
Inference
    ↓
Post-processing (interpret results)
    ↓
AnalysisResult (predictions, confidence, metadata)
```

### Model Architecture

Each model inherits from `BaseModel`:

```python
class BaseModel:
    def predict(self, image: np.ndarray) -> Dict:
        """Returns predictions dict"""
```

Models should return:
```python
{
    "predictions": {...},      # Main predictions
    "confidence": {...},       # Confidence scores
    "metadata": {...}          # Optional metadata
}
```

## Key Classes

### ImageAnalyzer
- Main entry point for analysis
- Manages model loading and inference
- Handles batch processing

### ModelLoader
- Registry of available models
- Model metadata management
- Downloads and caching

### ImagePreprocessor
- Handles image loading and validation
- Resizing and normalization
- Contrast enhancement

### AnalysisResult
- Immutable result container
- Serialization to JSON
- Metadata tracking

## Adding Model Support

### Step 1: Create Model Class
```python
# In mia/core/model_loader.py
class NewModel(BaseModel):
    def __init__(self):
        super().__init__("model-id", "model_type")
    
    def predict(self, image: np.ndarray) -> Dict:
        # Implement prediction logic
        return {"predictions": {...}}
```

### Step 2: Register Model
```python
# In ModelLoader
MODEL_REGISTRY = {
    "new-model": NewModel,
    ...
}

MODEL_METADATA = {
    "new-model": {
        "description": "...",
        "accuracy": 0.xx,
        "status": "beta",
        "supported_formats": ["PNG", "JPG"],
        "input_size": (256, 256)
    }
}
```

### Step 3: Write Tests
```python
def test_new_model_predict():
    model = NewModel()
    result = model.predict(dummy_image)
    assert "predictions" in result
```

### Step 4: Document
- Add to docs/MODELS.md
- Include example usage
- Note any specific requirements

## Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test with Sample Images
```python
from PIL import Image
import numpy as np

# Create test image
img = Image.new('L', (256, 256))
analyzer.analyze_image(img, "chest-xray")
```

## Performance Optimization

### Profiling
```bash
python -m cProfile -s cumtime your_script.py
```

### Memory Usage
```python
import tracemalloc
tracemalloc.start()
# Your code
current, peak = tracemalloc.get_traced_memory()
```

## CI/CD Pipeline

Our GitHub Actions workflow:
1. Runs tests on Python 3.9, 3.10, 3.11
2. Checks code style and types
3. Builds documentation
4. Calculates coverage

## Documentation Standards

### Docstring Format (Google Style)
```python
def function(param1: str) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
        
    Example:
        >>> function("test")
        True
    """
```

## Release Process

1. Update version in `mia/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. GitHub Action automatically builds and publishes

## Getting Help

- **Documentation**: See docs/ folder
- **Issues**: Check GitHub Issues
- **Discord**: Join community server
- **Email**: dev@example.com

## Resources

- [Python docs](https://docs.python.org/3/)
- [pytest documentation](https://docs.pytest.org/)
- [NumPy guide](https://numpy.org/doc/)
- [Medical Imaging Concepts](https://en.wikipedia.org/wiki/Medical_imaging)
