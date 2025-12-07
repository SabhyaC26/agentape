# Contributing to agentape

Thank you for your interest in contributing to agentape! We welcome contributions from the community.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Git

### Setting Up Your Development Environment

1. **Install uv** (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/agentape.git
   cd agentape
   ```

3. **Create a virtual environment and install dependencies**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

   This installs agentape in editable mode with all development dependencies.

## Development Workflow

> **Note**: We use `uv` for fast dependency management. It's significantly faster than pip and handles virtual environments seamlessly.

### Running Tests

We use pytest for testing. Run the full test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest tests/ --cov=agentape --cov-report=html
```

### Code Quality

We use several tools to maintain code quality:

**Linting with Ruff**:
```bash
ruff check agentape/ tests/
```

**Type checking with mypy**:
```bash
mypy agentape/
```

**Auto-formatting**:
```bash
ruff format agentape/ tests/
```

### Making Changes

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and add tests

3. **Run tests and linting**:
   ```bash
   pytest tests/
   ruff check agentape/ tests/
   mypy agentape/
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

## Contribution Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function signatures
- Write docstrings for public functions and classes
- Keep line length to 88 characters (enforced by Ruff)

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable

### Testing

- Write tests for all new features
- Ensure all tests pass before submitting a PR
- Aim for high test coverage (we target 80%+)
- Include both unit tests and integration tests where appropriate

### Documentation

- Update the README.md if you add new features
- Add docstrings to new functions and classes
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format

## Types of Contributions

### Bug Reports

If you find a bug, please open an issue with:
- A clear title and description
- Steps to reproduce the bug
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)

### Feature Requests

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you have

### Code Contributions

We especially welcome contributions in these areas:
- Bug fixes
- New features (discuss in an issue first for large features)
- Documentation improvements
- Test coverage improvements
- Performance optimizations

## Project Structure

```
agentape/
├── agentape/           # Main package
│   ├── clients/        # Client wrappers (OpenAI, etc.)
│   ├── core/           # Core functionality (tape, recorder, replayer)
│   ├── storage/        # Tape storage implementations
│   └── pytest_plugin.py
├── tests/              # Test suite
├── .agent/             # Workflow documentation
└── pyproject.toml      # Project configuration
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Reach out to the maintainers

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## License

By contributing to agentape, you agree that your contributions will be licensed under the MIT License.
