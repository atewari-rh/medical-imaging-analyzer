"""
Unit tests for CLI commands and help text
"""

from click.testing import CliRunner
from mia.cli import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Medical Imaging Analyzer - Privacy-first medical image analysis." in result.output
    assert "Examples:" in result.output
    assert "mia analyze --image chest.png --model chest-xray" in result.output
    assert "analyze" in result.output
    assert "batch" in result.output
    assert "models" in result.output
    assert "info" in result.output


def test_analyze_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Analyze a single medical image." in result.output
    assert "mia analyze --image chest.png --model chest-xray --output result.json" in result.output
    assert "Common Errors and Solutions:" in result.output
    assert "File not found" in result.output
    assert "--image" in result.output
    assert "--model" in result.output
    assert "--output" in result.output
    assert "--no-preprocessing" in result.output


def test_batch_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["batch", "--help"])
    assert result.exit_code == 0
    assert "Analyze multiple medical images in batch mode." in result.output
    assert "Examples:" in result.output
    assert (
        "mia batch --input-dir ./scans --output-dir ./results --model chest-xray" in result.output
    )
    assert "Common Errors and Solutions:" in result.output
    assert "--input-dir" in result.output
    assert "--output-dir" in result.output
    assert "--model" in result.output


def test_models_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["models", "--help"])
    assert result.exit_code == 0
    assert "List available medical analysis models" in result.output
    assert "Examples:" in result.output
    assert "mia models" in result.output


def test_info_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "--help"])
    assert result.exit_code == 0
    assert "Display application information" in result.output
    assert "Examples:" in result.output
    assert "mia info" in result.output


def test_info_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "=== Medical Imaging Analyzer ===" in result.output
    assert "Supported Modalities:" in result.output


def test_models_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["models"])
    assert result.exit_code == 0
    assert "=== Available Models ===" in result.output
    assert "chest-xray" in result.output
