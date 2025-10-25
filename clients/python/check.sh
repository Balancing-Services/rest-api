#!/bin/bash

# Script to run all quality checks for the Python client
# Runs tests, linting, type checking, and build verification

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to Python client directory
cd "$(dirname "$0")"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Python Client Quality Checks${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Generate pyproject.toml from draft
echo -e "${YELLOW}► Generating pyproject.toml...${NC}"
./generate-pyproject.sh
echo ""

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

# Run linting (exclude generated code)
echo -e "${YELLOW}► Running linter (ruff)...${NC}"
uv run --extra dev ruff check . --exclude balancing_services
echo -e "${GREEN}✓ Linting completed (generated code excluded)${NC}"
echo ""

# Run type checking
echo -e "${YELLOW}► Running type checker (mypy)...${NC}"
uv run --extra dev mypy balancing_services
echo -e "${GREEN}✓ Type checking passed${NC}"
echo ""

# Verify build
echo -e "${YELLOW}► Verifying build...${NC}"
uv build
echo -e "${GREEN}✓ Build successful${NC}"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}All quality checks passed!${NC}"
echo -e "${BLUE}========================================${NC}"
