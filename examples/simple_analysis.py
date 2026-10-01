"""
Simple example - Analyze a single medical image
"""

from mia import ImageAnalyzer

# Initialize analyzer
analyzer = ImageAnalyzer()

# Display available models
print("Available models:")
for model_name in analyzer.get_available_models():
    info = analyzer.get_model_info(model_name)
    print(f"  - {model_name}: {info['description']}")

# Analyze an image (you need to provide your own image)
# image_path = "path/to/your/xray.png"
# result = analyzer.analyze(image_path, "chest-xray")

# print("\nAnalysis Results:")
# print(f"Model: {result.model_name}")
# print(f"Processing time: {result.processing_time:.2f}s")
# print(f"Predictions: {result.predictions}")
# print(f"Confidence scores: {result.confidence_scores}")
