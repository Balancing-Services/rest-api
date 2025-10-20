# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **public specification repository** containing the OpenAPI specification for the Balancing Services REST API. This repository is the canonical source of truth for the API specification that is referenced by the private implementation repository.

**Important:** This repository contains ONLY the API specification and public documentation. It does NOT contain any implementation code, server infrastructure, or private components.

## Repository Structure

- `openapi.yaml` - The canonical OpenAPI 3.0.3 specification (source of truth)
- `README.md` - Public-facing documentation for API users
- `CHANGELOG.md` - Version history following Keep a Changelog format
- `LICENSE` - MIT License
- `.gitignore` - Standard ignore patterns

## Working with openapi.yaml

### Updating the Specification

- **Version updates:** When updating the API version, edit the `info.version` field in openapi.yaml
- **Maintain backwards compatibility:** Follow semantic versioning strictly

## Maintaining Documentation

### README.md Philosophy

**Keep README.md minimal and avoid duplication.** The README should NOT contain details that:
- Are already in openapi.yaml (endpoint lists, parameter details, area codes, etc.)
- Will become outdated quickly (version numbers, specific feature counts, detailed tables)

The README should focus on:
- How to get started with the API
- Where to find the complete specification
- How to get an API token
- Contact information

### CHANGELOG.md

- Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format
- Document all changes under appropriate categories (Added, Changed, Deprecated, Removed, Fixed, Security)
- Update version links at the bottom when creating new releases

## Versioning and Releases

This project follows [Semantic Versioning](https://semver.org/):
- **Major version (X.0.0):** Breaking changes to the API
- **Minor version (0.X.0):** New features, backward compatible
- **Patch version (0.0.X):** Bug fixes and minor improvements

### Release Process

1. Update version in `openapi.yaml` (info.version field)
2. Update CHANGELOG.md with release date and version
3. Commit changes
4. Create annotated git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
5. Push commit and tag: `git push origin main && git push origin vX.Y.Z`

## Git Workflow

- **Main branch:** Always contains the latest stable version
- **Tags:** Use annotated tags for versions (v1.0.0, v1.1.0, etc.)
- **Commit messages:** Do NOT include Claude Code attribution or AI-generated markers unless explicitly requested

## API Specification Standards

The API follows these standards:
- OpenAPI 3.0.3
- RFC 7807 Problem Details for error responses
- Bearer token authentication
- Cursor-based pagination for large datasets (bids endpoints)
- UTC timestamps for all time-based parameters
- Semantic versioning for API versions
