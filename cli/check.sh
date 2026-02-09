#!/bin/bash

# Script to run all quality checks for the CLI
# Runs tests, linting, and build verification

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to CLI directory
cd "$(dirname "$0")"

# Parse command line arguments
SKIP_GENERATE=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-generate)
            SKIP_GENERATE=true
            shift
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            echo "Use --skip-generate to skip pyproject.toml generation"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running CLI Quality Checks${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Generate pyproject.toml from draft
if [ "$SKIP_GENERATE" = false ]; then
    echo -e "${YELLOW}► Generating pyproject.toml...${NC}"
    ./generate-pyproject.sh
    echo ""
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed${NC}"
    echo "Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Run tests
echo -e "${YELLOW}► Running tests...${NC}"
uv run --extra dev pytest
echo -e "${GREEN}✓ Tests passed${NC}"
echo ""

# Run linting
echo -e "${YELLOW}► Running linter (ruff)...${NC}"
uv run --extra dev ruff check .
echo -e "${GREEN}✓ Linting passed${NC}"
echo ""

# Verify build
echo -e "${YELLOW}► Verifying build...${NC}"
uv build
echo -e "${GREEN}✓ Build successful${NC}"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}All quality checks passed!${NC}"
echo -e "${BLUE}========================================${NC}"
