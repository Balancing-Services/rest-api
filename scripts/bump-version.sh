#!/bin/bash

# Script to bump version across the repository
# Updates openapi.yaml, pyproject.toml, and CHANGELOG.md

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to repository root
cd "$(dirname "$0")/.."

# Check arguments
if [ $# -ne 1 ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 <version>"
    echo "Example: $0 1.2.0"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format (X.Y.Z)
if ! echo "$NEW_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
    echo -e "${RED}Error: Invalid version format${NC}"
    echo "Version must be in format X.Y.Z (e.g., 1.2.0)"
    exit 1
fi

# Get current version from openapi.yaml
CURRENT_VERSION=$(grep '^  version:' openapi.yaml | sed 's/  version: //')

echo -e "${YELLOW}Bumping version from ${CURRENT_VERSION} to ${NEW_VERSION}${NC}"
echo ""

# Update openapi.yaml
echo "Updating openapi.yaml..."
sed -i "s/^  version: .*/  version: ${NEW_VERSION}/" openapi.yaml

# Update CHANGELOG.md - add new Unreleased section and set date for current version
echo "Updating CHANGELOG.md..."
CURRENT_DATE=$(date +%Y-%m-%d)

# Create temporary file with updated changelog
{
    # Print everything up to and including the "## [Unreleased]" line
    sed -n '1,/^## \[Unreleased\]/p' CHANGELOG.md

    # Add empty line for new unreleased content
    echo ""

    # Add new version section
    echo "## [${NEW_VERSION}] - ${CURRENT_DATE}"

    # Print everything after the "## [Unreleased]" line (skipping it and the blank line)
    sed -n '/^## \[Unreleased\]/,$p' CHANGELOG.md | tail -n +2
} > CHANGELOG.md.tmp

mv CHANGELOG.md.tmp CHANGELOG.md

# Update version comparison links at the bottom of CHANGELOG.md
# Find the last version link and update the Unreleased comparison
sed -i "s|\[Unreleased\]: .*|\[Unreleased\]: https://github.com/balancing-services/rest-api/compare/v${NEW_VERSION}...HEAD|" CHANGELOG.md

# Add new version comparison link after Unreleased
sed -i "/^\[Unreleased\]:/a [${NEW_VERSION}]: https://github.com/balancing-services/rest-api/compare/v${CURRENT_VERSION}...v${NEW_VERSION}" CHANGELOG.md

echo ""
echo -e "${GREEN}✓ Version updated successfully${NC}"
echo ""
echo "Files modified:"
echo "  - openapi.yaml"
echo "  - CHANGELOG.md"
echo ""
echo "Note: pyproject.toml will be auto-generated from pyproject.toml.draft"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review the changes with: git diff"
echo "  2. Edit CHANGELOG.md to add release notes under [${NEW_VERSION}]"
echo "  3. Commit the changes with: git add -A && git commit -m 'Bump version to ${NEW_VERSION}'"
echo "  4. Run quality checks: ./clients/python/check.sh"
echo "  5. Publish with: cd clients/python && ./test-and-publish.sh"
