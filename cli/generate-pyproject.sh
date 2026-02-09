#!/bin/bash

# Script to generate pyproject.toml from pyproject.toml.draft
# Reads version from openapi.yaml and replaces __VERSION__, __DEP_LOWER__, __DEP_UPPER__ placeholders

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to CLI directory
cd "$(dirname "$0")"

# Parse command line arguments
SUFFIX=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --suffix)
            SUFFIX="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --suffix SUFFIX  Append PEP 440 suffix to version (e.g., a1, b2, rc1)"
            echo "  --help, -h       Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if pyproject.toml.draft exists
if [ ! -f "pyproject.toml.draft" ]; then
    echo -e "${RED}Error: pyproject.toml.draft not found${NC}"
    echo "Expected location: cli/pyproject.toml.draft"
    exit 1
fi

# Check if openapi.yaml exists
if [ ! -f "../openapi.yaml" ]; then
    echo -e "${RED}Error: openapi.yaml not found${NC}"
    exit 1
fi

# Extract version from openapi.yaml
VERSION=$(grep '^  version:' ../openapi.yaml | sed 's/  version: //' | tr -d ' ')

if [ -z "$VERSION" ]; then
    echo -e "${RED}Error: Could not extract version from openapi.yaml${NC}"
    exit 1
fi

# Parse major.minor.patch
MAJOR=$(echo "$VERSION" | cut -d. -f1)
MINOR=$(echo "$VERSION" | cut -d. -f2)

# Compute dependency bounds
DEP_LOWER="${MAJOR}.${MINOR}.0"
DEP_UPPER="${MAJOR}.$((MINOR + 1)).0"

# Apply suffix to package version (PEP 440)
PACKAGE_VERSION="${VERSION}"
if [ -n "$SUFFIX" ]; then
    PACKAGE_VERSION="${VERSION}${SUFFIX}"
fi

# Generate pyproject.toml from draft
echo -e "${YELLOW}Generating pyproject.toml with version ${PACKAGE_VERSION}...${NC}"
sed -e "s/version = __VERSION__/version = \"${PACKAGE_VERSION}\"/" \
    -e "s/__DEP_LOWER__/${DEP_LOWER}/g" \
    -e "s/__DEP_UPPER__/${DEP_UPPER}/g" \
    pyproject.toml.draft > pyproject.toml

echo -e "${GREEN}✓ Generated pyproject.toml (balancing-services>=${DEP_LOWER},<${DEP_UPPER})${NC}"
