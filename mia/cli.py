"""
Command-line interface for Medical Imaging Analyzer
"""

import click
import logging
import json
from pathlib import Path
from typing import Optional

from mia.core import ImageAnalyzer, ModelLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Medical Imaging Analyzer - Privacy-first medical image analysis"""
    pass


@cli.command()
@click.option(
    '--image',
    type=click.Path(exists=True),
    required=True,
    help='Path to medical image file'
)
@click.option(
    '--model',
    type=str,
    default='chest-xray',
    help='Model to use for analysis'
)
@click.option(
    '--output',
    type=click.Path(),
    help='Output file for results (JSON)'
)
@click.option(
    '--no-preprocessing',
    is_flag=True,
    help='Skip image preprocessing'
)
def analyze(image: str, model: str, output: Optional[str], no_preprocessing: bool):
    """Analyze a single medical image"""
    try:
        analyzer = ImageAnalyzer()
        
        # Check if model is available
        available = analyzer.get_available_models()
        if model not in available:
            click.secho(
                f"Error: Model '{model}' not found. Available: {', '.join(available)}",
                fg='red'
            )
            return
        
        click.secho(f"Analyzing image with model: {model}", fg='blue')
        
        result = analyzer.analyze(
            image,
            model,
            preprocessing=not no_preprocessing
        )
        
        # Display results
        click.secho("\n=== Analysis Results ===", fg='green', bold=True)
        click.echo(f"Image: {result.image_path}")
        click.echo(f"Model: {result.model_name}")
        click.echo(f"Processing Time: {result.processing_time:.2f}s")
        click.echo("\nPredictions:")
        
        for key, value in result.predictions.items():
            if isinstance(value, (int, float)):
                click.echo(f"  {key}: {value:.2%}" if value < 1 else f"  {key}: {value}")
            else:
                click.echo(f"  {key}: {value}")
        
        click.echo("\nConfidence Scores:")
        for key, value in result.confidence_scores.items():
            if isinstance(value, (int, float)):
                click.echo(f"  {key}: {value:.2%}" if value < 1 else f"  {key}: {value}")
            else:
                click.echo(f"  {key}: {value}")
        
        # Save results if output specified
        if output:
            with open(output, 'w') as f:
                json.dump(result.to_dict(), f, indent=2)
            click.secho(f"\nResults saved to: {output}", fg='green')
        
        click.secho("\n⚠️  DISCLAIMER: This is an AI-assisted analysis only.", fg='yellow')
        click.secho("Always consult qualified healthcare professionals for medical decisions.", fg='yellow')
        
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')
        exit(1)


@cli.command()
@click.option(
    '--input-dir',
    type=click.Path(exists=True),
    required=True,
    help='Directory containing medical images'
)
@click.option(
    '--output-dir',
    type=click.Path(),
    required=True,
    help='Directory to save results'
)
@click.option(
    '--model',
    type=str,
    default='chest-xray',
    help='Model to use for analysis'
)
def batch(input_dir: str, output_dir: str, model: str):
    """Analyze multiple medical images in batch mode"""
    try:
        analyzer = ImageAnalyzer()
        
        # Check if model is available
        available = analyzer.get_available_models()
        if model not in available:
            click.secho(
                f"Error: Model '{model}' not found. Available: {', '.join(available)}",
                fg='red'
            )
            return
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        click.secho(f"Starting batch analysis with model: {model}", fg='blue')
        
        results = analyzer.batch_analyze(input_dir, model)
        
        # Save results
        output_file = Path(output_dir) / "results.json"
        with open(output_file, 'w') as f:
            json.dump([r.to_dict() for r in results], f, indent=2)
        
        click.secho(f"\n=== Batch Analysis Complete ===", fg='green', bold=True)
        click.echo(f"Total images processed: {len(results)}")
        click.echo(f"Results saved to: {output_file}")
        
        # Summary statistics
        total_time = sum(r.processing_time for r in results)
        click.echo(f"Total processing time: {total_time:.2f}s")
        click.echo(f"Average time per image: {total_time/len(results):.2f}s")
        
        click.secho("\n⚠️  DISCLAIMER: This is an AI-assisted analysis only.", fg='yellow')
        click.secho("Always consult qualified healthcare professionals for medical decisions.", fg='yellow')
        
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')
        exit(1)


@cli.command()
def models():
    """List available models"""
    try:
        loader = ModelLoader()
        available = loader.get_available_models()
        
        click.secho("=== Available Models ===", fg='green', bold=True)
        
        for model_name in available:
            info = loader.get_model_info(model_name)
            click.echo(f"\n{model_name}:")
            click.echo(f"  Description: {info.get('description', 'N/A')}")
            click.echo(f"  Status: {info.get('status', 'N/A')}")
            click.echo(f"  Accuracy: {info.get('accuracy', 'N/A'):.0%}")
            click.echo(f"  Supported Formats: {', '.join(info.get('supported_formats', []))}")
        
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')
        exit(1)


@cli.command()
def info():
    """Display application information"""
    click.secho("=== Medical Imaging Analyzer ===", fg='green', bold=True)
    click.echo("Version: 0.1.0")
    click.echo("License: Apache License 2.0")
    click.echo("Privacy: All processing is local - no data uploaded")
    click.echo("\nSupported Modalities:")
    click.echo("  • Chest X-rays")
    click.echo("  • CT Scans (Lung)")
    click.echo("  • Ultrasound (Abdominal)")
    click.echo("  • X-rays (Fracture Detection)")
    click.echo("\nUsage:")
    click.echo("  Single image:   mia analyze --image <path> --model <model>")
    click.echo("  Batch:          mia batch --input-dir <dir> --output-dir <dir> --model <model>")
    click.echo("  List models:    mia models")
    click.echo("\n⚠️  IMPORTANT: Not approved for clinical diagnosis.")
    click.echo("Always consult qualified healthcare professionals.")


if __name__ == '__main__':
    cli()
