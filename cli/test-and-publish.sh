#!/bin/bash

# Script to publish CLI to TestPyPI, test it, and then publish to PyPI
#
# This script:
# 1. Runs quality checks
# 2. Publishes to TestPyPI
# 3. Creates test sandbox and installs from TestPyPI
# 4. Runs smoke tests against TestPyPI package
# 5. Prompts to publish to PyPI if tests pass
# 6. Publishes to production PyPI
# 7. Verifies production PyPI package works correctly

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to CLI directory and save the path
cd "$(dirname "$0")"
CLI_DIR="$(pwd)"

# Parse command line arguments
SKIP_CLI_TESTS=false
SKIP_TESTPYPI_UPLOAD=false
SUFFIX=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-cli-tests)
            SKIP_CLI_TESTS=true
            shift
            ;;
        --skip-testpypi-upload)
            SKIP_TESTPYPI_UPLOAD=true
            shift
            ;;
        --suffix)
            SUFFIX="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-cli-tests         Skip CLI smoke tests against live API (emergency use only)"
            echo "  --skip-testpypi-upload   Skip uploading to TestPyPI (assumes package already uploaded)"
            echo "  --suffix SUFFIX          Append PEP 440 suffix to version (e.g., a1, b2, rc1)"
            echo "  --help, -h               Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

PACKAGE_NAME="balancing-services-cli"
SANDBOX_DIR="/tmp/balancing-services-cli-test-sandbox-$$"

# Clean up leftovers from previous runs
rm -rf dist/
for old_dir in /tmp/balancing-services-cli-test-sandbox-* /tmp/balancing-services-cli-pypi-verify-*; do
    if [ -d "$old_dir" ]; then
        echo -e "${YELLOW}Removing leftover sandbox: ${old_dir}${NC}"
        rm -rf "$old_dir"
    fi
done

# Cleanup function
cleanup() {
    if [ -d "$SANDBOX_DIR" ]; then
        echo ""
        echo -e "${YELLOW}Cleaning up sandbox directory...${NC}"
        rm -rf "$SANDBOX_DIR"
        echo -e "${GREEN}✓ Cleanup complete${NC}"
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Helper function to install package with retry logic
# This will keep retrying until the package becomes available on the index
install_with_retry() {
    local max_retries=30  # 30 attempts * 10 seconds = 5 minutes max
    local retry=1
    local install_cmd="$@"

    while [ $retry -le $max_retries ]; do
        if [ $retry -eq 1 ]; then
            echo -e "${YELLOW}  Attempting installation (will retry if package not yet available)...${NC}"
        else
            echo -e "${YELLOW}  Retry ${retry}/${max_retries}...${NC}"
        fi

        if eval "$install_cmd" 2>&1; then
            echo -e "${GREEN}✓ Package installed successfully${NC}"
            return 0
        fi

        if [ $retry -lt $max_retries ]; then
            echo -e "${YELLOW}  Package not available yet, waiting 10 seconds before retry...${NC}"
            sleep 10
        fi
        ((retry++))
    done

    echo -e "${RED}✗ Installation failed after ${max_retries} attempts (5 minutes)${NC}"
    return 1
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}CLI Test & Publish Pipeline${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed${NC}"
    echo "Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Load .env file if it exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}Loading environment variables from .env...${NC}"
    set -a
    source .env
    set +a
    echo ""
fi

# Check environment variables
MISSING_VARS=()

if [ "$SKIP_CLI_TESTS" = false ] && [ -z "$BALANCING_SERVICES_API_KEY" ]; then
    MISSING_VARS+=("BALANCING_SERVICES_API_KEY")
fi

if [ "$SKIP_TESTPYPI_UPLOAD" = false ] && [ -z "$UV_PUBLISH_TOKEN_TESTPYPI" ]; then
    MISSING_VARS+=("UV_PUBLISH_TOKEN_TESTPYPI")
fi

if [ -z "$UV_PUBLISH_TOKEN_PYPI" ]; then
    MISSING_VARS+=("UV_PUBLISH_TOKEN_PYPI")
fi

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo -e "${RED}Error: Required environment variables not set${NC}"
    echo ""
    echo "Missing variables:"
    for var in "${MISSING_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "Please either:"
    echo "  1. Copy .env.sample to .env and fill in your credentials, or"
    echo "  2. Export the variables manually:"
    echo ""
    if [ "$SKIP_CLI_TESTS" = false ]; then
        echo "  export BALANCING_SERVICES_API_KEY='your-api-key'"
    fi
    echo "  export UV_PUBLISH_TOKEN_TESTPYPI='your-testpypi-token'"
    echo "  export UV_PUBLISH_TOKEN_PYPI='your-pypi-token'"
    echo ""
    echo "Get your credentials from:"
    if [ "$SKIP_CLI_TESTS" = false ]; then
        echo "  - API Key: https://balancing.services"
    fi
    echo "  - TestPyPI: https://test.pypi.org/manage/account/token/"
    echo "  - PyPI: https://pypi.org/manage/account/token/"
    echo ""
    if [ "$SKIP_CLI_TESTS" = false ]; then
        echo "Note: Use --skip-cli-tests to skip CLI testing (emergency use only)"
    fi
    exit 1
fi

# Warn if skipping CLI tests
if [ "$SKIP_CLI_TESTS" = true ]; then
    echo -e "${YELLOW}⚠ WARNING: Skipping live CLI tests${NC}"
    echo -e "${YELLOW}This should only be used in emergencies (e.g., API server is down)${NC}"
    echo -e "${YELLOW}The package will NOT be tested against the live API before publishing!${NC}"
    echo ""
    read -p "Are you sure you want to continue without CLI testing? (yes/no): " -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo -e "${YELLOW}Publishing cancelled${NC}"
        exit 0
    fi
    echo ""
fi

# Generate pyproject.toml from draft (with optional suffix)
echo -e "${YELLOW}► Generating pyproject.toml...${NC}"
if [ -n "$SUFFIX" ]; then
    ./generate-pyproject.sh --suffix "$SUFFIX"
else
    ./generate-pyproject.sh
fi
echo ""

# Get current version
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "//' | sed 's/"//')
echo -e "${BLUE}Package version: ${VERSION}${NC}"
echo ""

# Step 1: Run quality checks
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 1: Quality Checks${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

./check.sh --skip-generate

# Step 2: Publish to TestPyPI
if [ "$SKIP_TESTPYPI_UPLOAD" = false ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 2: Publishing to TestPyPI${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    echo -e "${YELLOW}► Publishing to TestPyPI...${NC}"
    UV_PUBLISH_TOKEN="$UV_PUBLISH_TOKEN_TESTPYPI" uv publish --publish-url https://test.pypi.org/legacy/

    echo -e "${GREEN}✓ Published to TestPyPI${NC}"
    echo ""
    echo "View at: https://test.pypi.org/project/${PACKAGE_NAME}/${VERSION}/"
    echo ""
else
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 2: Skipping TestPyPI Upload${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}⚠ Skipping TestPyPI upload (assuming version ${VERSION} already exists)${NC}"
    echo ""
fi

# Step 3: Create test sandbox
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 3: Creating Test Sandbox${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}► Creating sandbox directory: ${SANDBOX_DIR}${NC}"
mkdir -p "$SANDBOX_DIR"
cd "$SANDBOX_DIR"

echo -e "${YELLOW}► Creating virtual environment...${NC}"
uv venv

echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

# Step 4: Install from TestPyPI
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 4: Installing from TestPyPI${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}► Installing ${PACKAGE_NAME} from TestPyPI...${NC}"
if ! install_with_retry "uv --no-cache pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --index-strategy unsafe-best-match \"${PACKAGE_NAME}==${VERSION}\""; then
    echo -e "${RED}Error: Failed to install package from TestPyPI${NC}"
    exit 1
fi
echo ""

# Step 5: Run smoke tests
if [ "$SKIP_CLI_TESTS" = false ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 5: Running Smoke Tests${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    echo -e "${YELLOW}► Testing bs-cli --help...${NC}"
    if uv run bs-cli --help > /dev/null 2>&1; then
        echo -e "${GREEN}✓ bs-cli --help works${NC}"
    else
        echo -e "${RED}✗ bs-cli --help failed${NC}"
        exit 1
    fi
    echo ""

    echo -e "${YELLOW}► Testing bs-cli imbalance-prices against live API...${NC}"
    OUTPUT=$(uv run bs-cli --token "$BALANCING_SERVICES_API_KEY" imbalance-prices --area NL --start 2024-01-01T00:00:00Z --end 2024-01-01T01:00:00Z 2>&1)
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✓ bs-cli imbalance-prices executed successfully${NC}"
    elif echo "$OUTPUT" | grep -q -E "(Authentication failed|401)"; then
        echo -e "${RED}✗ Authentication failed - API key is invalid or expired${NC}"
        exit 1
    else
        echo -e "${RED}✗ bs-cli imbalance-prices failed${NC}"
        echo "$OUTPUT"
        exit 1
    fi

    echo ""
    echo -e "${GREEN}✓ All smoke tests passed${NC}"
    echo ""
else
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 5: Skipping Smoke Tests${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}⚠ CLI tests skipped - package not validated against live API${NC}"
    echo ""
fi

# Step 6: Prompt to publish to PyPI
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Step 6: Publish to PyPI${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${GREEN}TestPyPI testing completed successfully!${NC}"
echo ""
echo -e "${YELLOW}Ready to publish to production PyPI?${NC}"
echo ""
echo "This will publish ${PACKAGE_NAME} version ${VERSION} to PyPI."
echo ""

read -p "Publish to PyPI? (yes/no): " -r
echo ""

if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo -e "${YELLOW}Publishing to PyPI cancelled${NC}"
    echo ""
    echo "To publish manually later:"
    echo "  cd cli"
    echo "  UV_PUBLISH_TOKEN=\"\$UV_PUBLISH_TOKEN_PYPI\" uv publish"
    exit 0
fi

# Return to CLI directory for publishing
cd "$CLI_DIR"

echo -e "${YELLOW}► Publishing to PyPI...${NC}"
UV_PUBLISH_TOKEN="$UV_PUBLISH_TOKEN_PYPI" uv publish

echo ""
echo -e "${GREEN}✓ Successfully published to PyPI!${NC}"
echo ""
echo "View at: https://pypi.org/project/${PACKAGE_NAME}/${VERSION}/"
echo ""

# Step 7: Verify PyPI package
if [ "$SKIP_CLI_TESTS" = false ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 7: Verify PyPI Package${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    echo -e "${YELLOW}► Verifying production PyPI package...${NC}"
    echo ""

    # Create new sandbox for PyPI verification
    PYPI_SANDBOX_DIR="/tmp/balancing-services-cli-pypi-verify-$$"
    mkdir -p "$PYPI_SANDBOX_DIR"
    cd "$PYPI_SANDBOX_DIR"

    echo -e "${YELLOW}► Creating verification environment...${NC}"
    uv venv
    echo -e "${GREEN}✓ Environment created${NC}"
    echo ""

    echo -e "${YELLOW}► Installing ${PACKAGE_NAME} from production PyPI...${NC}"
    if ! install_with_retry "uv --no-cache pip install \"${PACKAGE_NAME}==${VERSION}\""; then
        echo -e "${RED}Error: Failed to install package from PyPI${NC}"
        exit 1
    fi
    echo ""

    VERIFICATION_FAILED=false

    echo -e "${YELLOW}► Testing bs-cli --help...${NC}"
    if uv run bs-cli --help > /dev/null 2>&1; then
        echo -e "${GREEN}✓ bs-cli --help works with PyPI package${NC}"
    else
        echo -e "${RED}✗ bs-cli --help failed with PyPI package${NC}"
        VERIFICATION_FAILED=true
    fi

    echo -e "${YELLOW}► Testing bs-cli imbalance-prices...${NC}"
    OUTPUT=$(uv run bs-cli --token "$BALANCING_SERVICES_API_KEY" imbalance-prices --area NL --start 2024-01-01T00:00:00Z --end 2024-01-01T01:00:00Z 2>&1)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ bs-cli imbalance-prices works with PyPI package${NC}"
    else
        echo -e "${RED}✗ bs-cli imbalance-prices failed with PyPI package${NC}"
        VERIFICATION_FAILED=true
    fi

    # Cleanup PyPI sandbox
    cd /
    rm -rf "$PYPI_SANDBOX_DIR"

    echo ""
    if [ "$VERIFICATION_FAILED" = true ]; then
        echo -e "${RED}✗ PyPI package verification FAILED${NC}"
        echo -e "${RED}The package was published but may have issues!${NC}"
        echo ""
    else
        echo -e "${GREEN}✓ PyPI package verified successfully!${NC}"
        echo ""
    fi
fi

echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Create git tag: git tag -a v${VERSION} -m 'Release v${VERSION}'"
echo "  2. Push tag: git push origin v${VERSION}"
echo "  3. Create GitHub release at: https://github.com/balancing-services/rest-api/releases/new"
