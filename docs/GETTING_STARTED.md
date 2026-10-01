# Getting Started with Medical Imaging Analyzer

## Quick Start (5 minutes)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/medical-imaging-analyzer/mia.git
cd mia

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### 2. Verify Installation

```bash
# Check if installation worked
mia info
```

You should see the Medical Imaging Analyzer information displayed.

### 3. Analyze Your First Image

```bash
# Analyze a single image
mia analyze --image path/to/your/xray.png --model chest-xray
```

The tool will output predictions and confidence scores.

## First Analysis Example

### Using the Command Line

```bash
# See available models
mia models

# Analyze an X-ray image
mia analyze --image patient_xray.png --model chest-xray --output result.json

# Batch analyze a directory of images
mia batch --input-dir ./x-rays --output-dir ./results --model chest-xray
```

### Using Python API

```python
from mia import ImageAnalyzer

# Create analyzer
analyzer = ImageAnalyzer()

# Check available models
print("Available models:", analyzer.get_available_models())

# Analyze a single image
result = analyzer.analyze("xray.png", "chest-xray")

print("Predictions:", result.predictions)
print("Confidence:", result.confidence_scores)
print("Processing time:", result.processing_time, "seconds")

# Save results to JSON
with open("result.json", "w") as f:
    f.write(result.to_json_string())
```

## Supported Models

| Model | Use Case | Accuracy | Status |
|-------|----------|----------|--------|
| `chest-xray` | Chest X-ray classification | 95% | ✅ Ready |
| `ct-lung` | CT lung nodule detection | 92% | ✅ Ready |
| `ultrasound-ab` | Abdominal ultrasound analysis | 88% | 🔄 Beta |
| `fracture-detect` | Fracture detection in X-rays | 90% | 🔄 Beta |

## Common Tasks

### Batch Processing Multiple Images

```bash
# Process all images in a directory
mia batch \
  --input-dir ./medical_images \
  --output-dir ./analysis_results \
  --model chest-xray
```

### Programmatic Usage with Custom Models

```python
from mia import ImageAnalyzer
from pathlib import Path

analyzer = ImageAnalyzer()

# Process multiple images
image_dir = Path("./images")
for image_file in image_dir.glob("*.png"):
    result = analyzer.analyze(str(image_file), "chest-xray")
    print(f"{image_file.name}: {result.predictions}")
```

### Processing with Different Models

```python
from mia import ImageAnalyzer

analyzer = ImageAnalyzer()

# CT Scan analysis
ct_result = analyzer.analyze("ct_scan.png", "ct-lung")

# Fracture detection
fracture_result = analyzer.analyze("xray_arm.png", "fracture-detect")

# Ultrasound analysis
us_result = analyzer.analyze("ultrasound.png", "ultrasound-ab")
```

## File Formats

### Supported Image Types
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- TIFF (`.tiff`, `.tif`)
- BMP (`.bmp`)

### Output Format

Analysis results are returned as:
```json
{
  "image_path": "path/to/image.png",
  "model": "chest-xray",
  "predictions": {
    "Normal": 0.75,
    "Pneumonia": 0.15,
    "Tuberculosis": 0.05,
    "COVID-19": 0.02,
    "Other Abnormality": 0.03
  },
  "confidence_scores": {
    "primary_prediction": "Normal",
    "confidence_score": 0.75,
    "recommendation": "No significant findings detected"
  },
  "processing_time": 1.23,
  "metadata": {
    "image_size": [512, 512],
    "preprocessing_applied": true
  }
}
```

## Performance Tips

1. **Batch Processing**: Use batch mode for multiple images - it's faster
2. **Image Preprocessing**: Enable preprocessing for best results (default: on)
3. **Memory**: For large batches, process in smaller chunks
4. **GPU**: The current version uses CPU, but GPU support is planned

## Troubleshooting

### "Module not found" error

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall the package
pip install -e .
```

### Image not recognized

```bash
# Verify the image format is supported
# Supported: PNG, JPG, TIFF, BMP

# Try converting your image
# From terminal/command line:
# macOS/Linux: sips -s format png image.bmp -o image.png
# Windows: Use an image editor or ImageMagick
```

### Slow analysis

```bash
# Skip preprocessing if images are already processed
mia analyze --image image.png --model chest-xray --no-preprocessing

# Use batch processing instead of individual analyses
mia batch --input-dir ./images --output-dir ./results --model chest-xray
```

## Next Steps

- **Learn the API**: See [docs/API.md](../docs/API.md)
- **Contribute**: See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Develop**: See [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md)
- **Models**: See [docs/MODELS.md](../docs/MODELS.md) for detailed model info

## Important Disclaimers

⚠️ **Medical Use Disclaimer**

This tool provides AI-assisted analysis only. It is:
- NOT a substitute for professional medical diagnosis
- NOT approved for clinical diagnosis in any jurisdiction
- A tool to assist medical professionals, not replace them

Always consult qualified healthcare professionals for diagnosis and treatment.

## Getting Help

- **Documentation**: Check the `docs/` folder
- **Issues**: Create a GitHub issue for bugs or features
- **Examples**: See the `examples/` folder
- **Discord**: Join our community server
- **Email**: help@example.com

---

Ready to get started? Run your first analysis now! 🚀
