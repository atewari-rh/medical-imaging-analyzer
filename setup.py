"""
Setup configuration for Medical Imaging Analyzer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="medical-imaging-analyzer",
    version="0.1.0",
    author="Medical Imaging Analyzer Contributors",
    description="Privacy-first medical image analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/medical-imaging-analyzer/mia",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Healthcare",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "scikit-image>=0.21.0",
        "click>=8.1.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "mia=mia.cli:cli",
        ],
    },
    keywords="medical-imaging healthcare AI analysis",
    project_urls={
        "Bug Reports": "https://github.com/medical-imaging-analyzer/mia/issues",
        "Documentation": "https://mia-docs.example.com",
        "Source Code": "https://github.com/medical-imaging-analyzer/mia",
    },
)
