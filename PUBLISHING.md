# PyPI Publishing Quick Reference

## One-Time Setup

1. **Install build tools**:
   ```bash
   pip install --upgrade build twine
   ```

2. **Create PyPI account**: https://pypi.org/account/register/

3. **Generate API token**: https://pypi.org/manage/account/token/

## Publishing Steps

```bash
# 1. Update version in pyproject.toml
# version = "0.1.0" -> "0.1.1" (or whatever)

# 2. Clean previous builds
rm -rf dist/ build/ *.egg-info

# 3. Build the package
python -m build

# 4. Verify the package (optional but recommended)
python -m twine check dist/*

# 5. Upload to PyPI
python -m twine upload dist/*
# Username: __token__
# Password: <your-pypi-token>

# 6. Test installation
pip install agentape
```

## Pre-Release Checklist

- [ ] Tests pass: `pytest tests/`
- [ ] Version updated in `pyproject.toml`
- [ ] README is current
- [ ] LICENSE file exists
- [ ] Package verified: `python -m twine check dist/*`
- [ ] Tested locally

## After Publishing

```bash
# Tag the release
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

---

For detailed instructions, see: `.agent/workflows/publish-to-pypi.md`
