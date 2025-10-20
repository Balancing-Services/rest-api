#!/bin/bash

# Script to generate Python client from OpenAPI specification
# Uses uvx to run openapi-python-client without installing it

set -e

# Navigate to the script directory
cd "$(dirname "$0")"

# Check if OpenAPI spec exists
if [ ! -f "../../openapi.yaml" ]; then
    echo "Error: OpenAPI spec not found at ../../openapi.yaml"
    exit 1
fi

# Check if uvx is available
if ! command -v uvx &> /dev/null; then
    echo "Error: uvx is not installed. Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if git working directory is clean (warning only)
if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "Warning: Git working directory has uncommitted changes"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Generation cancelled"
            exit 1
        fi
    fi
fi

# Remove existing generated code (if any)
if [ -d "balancing_services" ]; then
    echo "Removing existing generated code..."
    rm -rf balancing_services
fi

# Generate the client
echo "Generating Python client from OpenAPI spec..."
uvx openapi-python-client generate \
    --path ../../openapi.yaml \
    --config config.yaml \
    --meta none

echo "Client generation complete!"
echo "Generated code is in: balancing_services/"
