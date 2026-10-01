# Contributing to Medical Imaging Analyzer

Thank you for your interest in contributing to Medical Imaging Analyzer! We welcome contributions from everyone.

## Code of Conduct

Our community is dedicated to providing a welcoming and inclusive environment for all. We expect all contributors to:
- Be respectful and inclusive
- Focus on constructive feedback
- Report violations to [conduct@example.com]

## How to Contribute

### 1. Report Bugs

Found a bug? Please create an issue with:
- Clear, descriptive title
- Step-by-step reproduction
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### 2. Suggest Features

Feature suggestions are welcome! Include:
- Use case and motivation
- Proposed solution (if any)
- Alternative solutions considered

### 3. Submit Code Changes

#### Setup Development Environment

```bash
git clone https://github.com/medical-imaging-analyzer/mia.git
cd mia

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

#### Make Your Changes

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write or update tests
4. Ensure code quality:
   ```bash
   black mia tests
   flake8 mia tests
   mypy mia
   ```
5. Run tests: `pytest tests/`
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push and create a Pull Request

### 4. Writing Tests

We use pytest. Example test:

```python
import pytest
from mia.core import ImageAnalyzer

def test_analyzer_loads_model():
    analyzer = ImageAnalyzer()
    assert analyzer.load_model("chest-xray") == True
```

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=mia  # With coverage
```

### 5. Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update API documentation in docs/
- Include examples for new features

### 6. Adding a New Model

1. Create model class in `mia/core/model_loader.py`:
   ```python
   class MyModel(BaseModel):
       def __init__(self):
           super().__init__("my-model", "type")
       
       def predict(self, image):
           # Implementation
           return predictions
   ```

2. Register in `MODEL_REGISTRY` and `MODEL_METADATA`
3. Add tests
4. Update documentation

## Pull Request Process

1. Update documentation and tests
2. Ensure CI/CD passes
3. Request review from maintainers
4. Respond to feedback
5. Once approved, your PR will be merged

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints where possible
- Write clear variable names
- Max line length: 100 characters

### Commits
- Keep commits atomic and logical
- Use meaningful commit messages
- Format: `Type: Description` (e.g., "Feature: Add lung CT model")

### Privacy & Security
- Never commit API keys or credentials
- Use `.gitignore` for sensitive files
- Run security checks before submitting

### Medical/Healthcare Context
- Include disclaimers where necessary
- Ensure patient privacy is maintained
- Consider ethical implications

## Questions?

- Open an issue for technical questions
- Join our Discord community
- Email: contributors@example.com

## Recognition

Contributors will be listed in:
- README.md
- CONTRIBUTORS.md
- GitHub contributors page

Thank you for making Medical Imaging Analyzer better! 🙏
