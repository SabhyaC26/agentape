---
description: How to publish agentape to PyPI
---

# Publishing agentape to PyPI

## Prerequisites

1. **Create PyPI Account**
   - Sign up at https://pypi.org/account/register/
   - Verify your email address

2. **Generate API Token**
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token (scope: "Entire account" or specific to your project)
   - Save this token securely - you'll only see it once!

## Step-by-Step Publishing Process

### 1. Install Build Tools

```bash
pip install --upgrade build twine
```

### 2. Update Version Number

Edit `pyproject.toml` and update the version number:
```toml
version = "0.1.0"  # Change to your desired version
```

Follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### 3. Clean Previous Builds

```bash
rm -rf dist/ build/ *.egg-info
```

### 4. Build the Package

```bash
python -m build
```

This creates:
- `dist/agentape-X.Y.Z-py3-none-any.whl` (wheel distribution)
- `dist/agentape-X.Y.Z.tar.gz` (source distribution)

### 5. Verify the Package (Optional but Recommended)

Check that the package metadata is correct:
```bash
python -m twine check dist/*
```

This validates your package before uploading.

### 6. Publish to PyPI

```bash
python -m twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token (including `pypi-` prefix)

### 7. Verify Installation

```bash
pip install agentape
```

## Using .pypirc (Optional)

To avoid entering credentials each time, create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE
```

**Important**: Set proper permissions:
```bash
chmod 600 ~/.pypirc
```

## Automated Publishing with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: python -m twine upload dist/*
```

Add your PyPI token as a GitHub secret named `PYPI_API_TOKEN`.

## Pre-Release Checklist

- [ ] All tests pass (`pytest tests/`)
- [ ] Version number updated in `pyproject.toml`
- [ ] README.md is up to date
- [ ] CHANGELOG updated (if you have one)
- [ ] Package metadata verified (`python -m twine check dist/*`)
- [ ] Git tag created for the version

## Post-Release

1. **Create a Git Tag**:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

2. **Create GitHub Release** (if using GitHub):
   - Go to your repository's releases page
   - Create a new release from the tag
   - Add release notes

## Troubleshooting

### "File already exists" error
- You cannot re-upload the same version
- Increment the version number and rebuild

### Import errors after installation
- Check that `agentape/__init__.py` exports the right symbols
- Verify package structure with `tar -tzf dist/agentape-*.tar.gz`

### Missing dependencies
- Ensure all dependencies are listed in `pyproject.toml`
- Test in a fresh virtual environment
