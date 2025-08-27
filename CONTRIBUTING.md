# Contributing to C Struct YAML Generator

Thank you for your interest in contributing to this project! We welcome contributions of all kinds, from bug reports to feature implementations.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or bugfix
5. Make your changes
6. Add or update tests as needed
7. Ensure all tests pass
8. Submit a pull request

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix issues found in the codebase
- **Feature enhancements**: Add new functionality or improve existing features
- **Documentation**: Improve README, code comments, or add examples
- **Testing**: Add test cases or improve test coverage
- **Performance**: Optimize code for better performance
- **Code quality**: Refactor code for better maintainability

### Areas for Contribution

- **Parser improvements**: Enhance C parsing capabilities
- **Output formats**: Add support for JSON, XML, or other formats
- **Preprocessing**: Improve macro expansion and include handling
- **Error handling**: Better error messages and recovery
- **Platform support**: Ensure compatibility across different systems
- **Performance**: Optimize for large files or complex structures
- **Documentation**: Examples, tutorials, and API documentation

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- A text editor or IDE

### Environment Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ai_parse_structure.git
cd ai_parse_structure

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Verify installation
python pycparser_yaml_generator.py --help
python yaml_viewer.py --help
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_parser.py

# Run with verbose output
pytest -v
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (not 79)
- **Imports**: Use absolute imports when possible
- **Type hints**: Required for public APIs
- **Docstrings**: Use Google-style docstrings

### Code Formatting

We use `black` for automatic code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

### Linting

We use `flake8` for linting:

```bash
# Run linting
flake8 .

# Run with specific configuration
flake8 --max-line-length=100 .
```

### Type Checking

We use `mypy` for static type checking:

```bash
# Run type checking
mypy .

# Check specific file
mypy pycparser_yaml_generator.py
```

### Code Structure

- **Classes**: Use PascalCase
- **Functions/Methods**: Use snake_case
- **Constants**: Use UPPER_SNAKE_CASE
- **Private members**: Prefix with underscore
- **Type hints**: Use for all public APIs

### Documentation

- All public functions and classes must have docstrings
- Use Google-style docstrings
- Include parameter types and return types
- Provide usage examples for complex functions
- Keep comments concise and relevant

## Testing

### Test Structure

```
tests/
├── test_parser.py          # Core parsing tests
├── test_types.py           # Type analysis tests
├── test_output.py          # Output formatting tests
├── test_preprocessing.py   # Preprocessing tests
├── fixtures/               # Test data files
│   ├── simple.h
│   ├── complex.h
│   └── bitfields.h
└── expected/               # Expected output files
    ├── simple.yml
    ├── complex.yml
    └── bitfields.yml
```

### Writing Tests

- Use descriptive test names: `test_parse_nested_struct_with_bitfields`
- Test both positive and negative cases
- Use fixtures for test data
- Mock external dependencies when appropriate
- Aim for high test coverage (>90%)

### Test Categories

1. **Unit tests**: Test individual functions and methods
2. **Integration tests**: Test component interactions
3. **End-to-end tests**: Test complete workflows
4. **Performance tests**: Test with large files
5. **Regression tests**: Prevent known issues from returning

## Submitting Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-json-output`
- `bugfix/fix-bitfield-alignment`
- `docs/improve-readme`
- `refactor/reorganize-parser`

### Commit Messages

Follow conventional commit format:

```
type(scope): brief description

Longer description if needed.

Fixes #123
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests** for new features or bug fixes
3. **Ensure all tests pass** locally before submitting
4. **Update CHANGELOG.md** with your changes
5. **Write a clear PR description** explaining what and why
6. **Reference related issues** using "Fixes #123" or "Closes #123"

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for changes
- [ ] Updated existing tests

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Clear title** describing the issue
2. **Environment details** (OS, Python version, etc.)
3. **Steps to reproduce** the issue
4. **Expected behavior** vs actual behavior
5. **Sample code or files** that demonstrate the issue
6. **Error messages** or stack traces
7. **Relevant configuration** settings

### Feature Requests

For feature requests, please include:

1. **Clear description** of the proposed feature
2. **Use case** or problem it solves
3. **Proposed implementation** if you have ideas
4. **Examples** of how it would be used
5. **Alternative solutions** you've considered

### Issue Templates

```markdown
**Bug Report**

**Environment:**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python version: [e.g., 3.9.2]
- Tool version: [e.g., 1.0.0]

**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Additional Context:**
Any other relevant information
```

## Communication

- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions
- **Discussions**: For general questions and ideas

## Recognition

Contributors will be recognized in:

- CHANGELOG.md for significant contributions
- README.md contributors section
- Release notes for major features

Thank you for contributing to C Struct YAML Generator!
