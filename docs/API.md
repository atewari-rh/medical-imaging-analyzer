# API Reference

## Overview

Medical Imaging Analyzer provides both programmatic Python API and a command-line interface for analyzing medical images locally.

## Python API

### ImageAnalyzer

Main class for performing image analysis.

```python
from mia import ImageAnalyzer

analyzer = ImageAnalyzer(model_dir="/path/to/models")
```

#### Methods

##### `load_model(model_name: str) -> bool`

Load a model for analysis.

**Parameters:**
- `model_name` (str): Name of the model to load (e.g., "chest-xray")

**Returns:**
- `bool`: True if model loaded successfully

**Example:**
```python
if analyzer.load_model("chest-xray"):
    print("Model loaded")
```

##### `analyze(image_path: str, model_name: str, preprocessing: bool = True) -> AnalysisResult`

Analyze a single medical image.

**Parameters:**
- `image_path` (str): Path to the image file
- `model_name` (str): Name of the model to use
- `preprocessing` (bool): Whether to apply preprocessing (default: True)

**Returns:**
- `AnalysisResult`: Object containing predictions and metadata

**Example:**
```python
result = analyzer.analyze("xray.png", "chest-xray")
print(f"Predictions: {result.predictions}")
print(f"Confidence: {result.confidence_scores}")
print(f"Time: {result.processing_time:.2f}s")
```

##### `batch_analyze(image_dir: str, model_name: str, output_file: Optional[str] = None) -> List[AnalysisResult]`

Analyze multiple images from a directory.

**Parameters:**
- `image_dir` (str): Directory containing images
- `model_name` (str): Name of the model to use
- `output_file` (str, optional): File to save JSON results

**Returns:**
- `List[AnalysisResult]`: List of analysis results

**Example:**
```python
results = analyzer.batch_analyze(
    "./images",
    "chest-xray",
    output_file="results.json"
)
for result in results:
    print(f"{result.image_path}: {result.predictions}")
```

##### `get_available_models() -> List[str]`

Get list of available models.

**Returns:**
- `List[str]`: List of model names

**Example:**
```python
models = analyzer.get_available_models()
print(f"Available models: {models}")
```

##### `get_model_info(model_name: str) -> Dict[str, Any]`

Get information about a specific model.

**Parameters:**
- `model_name` (str): Name of the model

**Returns:**
- `Dict`: Model metadata including accuracy, status, supported formats

**Example:**
```python
info = analyzer.get_model_info("chest-xray")
print(f"Accuracy: {info['accuracy']}")
print(f"Status: {info['status']}")
```

### AnalysisResult

Container for analysis results.

#### Properties

- `image_path` (str): Path to the analyzed image
- `model_name` (str): Name of the model used
- `predictions` (Dict): Model predictions
- `confidence_scores` (Dict): Confidence scores
- `processing_time` (float): Processing time in seconds
- `metadata` (Dict): Additional metadata

#### Methods

##### `to_dict() -> Dict`

Convert result to dictionary.

**Returns:**
- `Dict`: Result as dictionary

##### `to_json_string() -> str`

Convert result to JSON string.

**Returns:**
- `str`: Result as JSON string

**Example:**
```python
result = analyzer.analyze("image.png", "chest-xray")
json_str = result.to_json_string()
print(json_str)
```

### ModelLoader

Model management and loading.

```python
from mia.core import ModelLoader

loader = ModelLoader()
```

#### Methods

##### `load_model(model_name: str) -> BaseModel`

Load a model.

**Parameters:**
- `model_name` (str): Name of the model

**Returns:**
- `BaseModel`: Model instance

##### `get_available_models() -> List[str]`

List all available models.

**Returns:**
- `List[str]`: Model names

##### `get_model_info(model_name: str) -> Dict[str, Any]`

Get model metadata.

**Parameters:**
- `model_name` (str): Name of the model

**Returns:**
- `Dict`: Model information

### ImagePreprocessor

Image preprocessing utilities.

```python
from mia.core import ImagePreprocessor

preprocessor = ImagePreprocessor(target_size=(256, 256))
```

#### Methods

##### `process(image: Image.Image) -> np.ndarray`

Apply preprocessing pipeline to image.

**Parameters:**
- `image` (PIL.Image): Input image

**Returns:**
- `np.ndarray`: Preprocessed image array

## Command-Line Interface

### Basic Usage

```bash
mia [COMMAND] [OPTIONS]
```

### Commands

#### `analyze` - Analyze single image

```bash
mia analyze --image <path> [--model <model>] [--output <file>] [--no-preprocessing]
```

**Options:**
- `--image` (required): Path to medical image
- `--model` (default: chest-xray): Model to use
- `--output` (optional): Output JSON file
- `--no-preprocessing`: Skip preprocessing

**Example:**
```bash
mia analyze --image xray.png --model chest-xray --output result.json
```

#### `batch` - Analyze multiple images

```bash
mia batch --input-dir <dir> --output-dir <dir> [--model <model>]
```

**Options:**
- `--input-dir` (required): Directory with images
- `--output-dir` (required): Output directory
- `--model` (default: chest-xray): Model to use

**Example:**
```bash
mia batch --input-dir ./images --output-dir ./results --model chest-xray
```

#### `models` - List available models

```bash
mia models
```

Shows all available models with details.

#### `info` - Show application information

```bash
mia info
```

## Usage Examples

### Basic Python Usage

```python
from mia import ImageAnalyzer

# Initialize
analyzer = ImageAnalyzer()

# List models
print(analyzer.get_available_models())

# Analyze image
result = analyzer.analyze("xray.png", "chest-xray")

# Access results
print(f"Predictions: {result.predictions}")
print(f"Confidence: {result.confidence_scores}")
```

### Batch Processing

```python
from mia import ImageAnalyzer
import json

analyzer = ImageAnalyzer()

# Process directory
results = analyzer.batch_analyze(
    image_dir="./medical_images",
    model_name="chest-xray",
    output_file="analysis_results.json"
)

# Process results
for result in results:
    print(f"Image: {result.image_path}")
    print(f"Result: {result.predictions}")
```

### Custom Model Integration

```python
from mia.core.model_loader import BaseModel
from mia import ImageAnalyzer
import numpy as np

# Create custom model
class MyModel(BaseModel):
    def __init__(self):
        super().__init__("my-model", "custom")
    
    def predict(self, image: np.ndarray):
        return {"predictions": {...}}

# Register and use
ModelLoader.MODEL_REGISTRY["my-model"] = MyModel
analyzer = ImageAnalyzer()
result = analyzer.analyze("image.png", "my-model")
```

## Error Handling

```python
from mia import ImageAnalyzer

try:
    analyzer = ImageAnalyzer()
    result = analyzer.analyze("image.png", "chest-xray")
    if "error" in result.predictions:
        print(f"Error: {result.predictions['error']}")
    else:
        print(f"Success: {result.predictions}")
except FileNotFoundError:
    print("Image file not found")
except Exception as e:
    print(f"Analysis failed: {str(e)}")
```

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- TIFF (.tiff, .tif)
- BMP (.bmp)

## Performance Considerations

- **Image Size**: Larger images take longer to process
- **Preprocessing**: Disable if images are pre-processed
- **Batch Processing**: More efficient than individual analyses
- **Memory**: Keep available RAM in mind for large batches

## Threading and Concurrency

For concurrent analysis:

```python
from concurrent.futures import ThreadPoolExecutor
from mia import ImageAnalyzer

analyzer = ImageAnalyzer()
images = ["img1.png", "img2.png", "img3.png"]

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(
        lambda img: analyzer.analyze(img, "chest-xray"),
        images
    ))
```

## Version Information

Current API Version: 0.1.0

This is an early release. API may change in future versions.
