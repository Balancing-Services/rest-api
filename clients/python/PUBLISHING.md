# Publishing to PyPI

## Prerequisites

- PyPI and TestPyPI accounts with API tokens
- `uv` installed: `pip install uv`

## Publishing Process

### 1. Pre-release checks

```bash
cd clients/python

# Update version in pyproject.toml
# Update CHANGELOG.md

# Run tests
uv run pytest

# Build
uv build
```

### 2. Publish to TestPyPI

```bash
export UV_PUBLISH_TOKEN="your-testpypi-token"
uv publish --publish-url https://test.pypi.org/legacy/
```

Test installation:
```bash
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ balancing-services
```

### 3. Publish to PyPI

```bash
export UV_PUBLISH_TOKEN="your-pypi-token"
uv publish
```

Test installation:
```bash
uv pip install balancing-services
```

### 4. Post-release

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Create GitHub release at https://github.com/balancing-services/rest-api/releases
