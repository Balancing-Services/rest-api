# Release Checklist

## Pre-release

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Run tests: `uv run pytest`
- [ ] Run linting: `uv run ruff check .`
- [ ] Run type checking: `uv run mypy balancing_services`
- [ ] Commit all changes

## Build & Test

- [ ] Build: `uv build`
- [ ] Verify wheel contents: `unzip -l dist/*.whl`
- [ ] Publish to TestPyPI: `export UV_PUBLISH_TOKEN="..." && uv publish --publish-url https://test.pypi.org/legacy/`
- [ ] Test installation: `uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ balancing-services`

## Release

- [ ] Publish to PyPI: `export UV_PUBLISH_TOKEN="..." && uv publish`
- [ ] Test installation: `uv pip install balancing-services`
- [ ] Create git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub release at https://github.com/balancing-services/rest-api/releases
