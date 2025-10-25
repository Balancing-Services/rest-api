#!/bin/bash

# Script to generate pyproject.toml from pyproject.toml.draft
# Reads version from openapi.yaml and replaces __VERSION__ placeholder

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to Python client directory
cd "$(dirname "$0")"

# Check if pyproject.toml.draft exists
if [ ! -f "pyproject.toml.draft" ]; then
    echo -e "${RED}Error: pyproject.toml.draft not found${NC}"
    echo "Expected location: clients/python/pyproject.toml.draft"
    exit 1
fi

# Check if openapi.yaml exists
if [ ! -f "../../openapi.yaml" ]; then
    echo -e "${RED}Error: openapi.yaml not found${NC}"
    exit 1
fi

# Extract version from openapi.yaml
VERSION=$(grep '^  version:' ../../openapi.yaml | sed 's/  version: //' | tr -d ' ')

if [ -z "$VERSION" ]; then
    echo -e "${RED}Error: Could not extract version from openapi.yaml${NC}"
    exit 1
fi

# Generate pyproject.toml from draft
echo -e "${YELLOW}Generating pyproject.toml with version ${VERSION}...${NC}"
sed "s/version = __VERSION__/version = \"${VERSION}\"/" pyproject.toml.draft > pyproject.toml

echo -e "${GREEN}✓ Generated pyproject.toml${NC}"
