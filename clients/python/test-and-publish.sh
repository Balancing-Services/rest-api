#!/bin/bash

# Script to publish Python client to TestPyPI, test it, and then publish to PyPI
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

# Navigate to Python client directory and save the path
cd "$(dirname "$0")"
PYTHON_CLIENT_DIR="$(pwd)"

# Parse command line arguments
SKIP_API_TESTS=false
SKIP_TESTPYPI_UPLOAD=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-api-tests)
            SKIP_API_TESTS=true
            shift
            ;;
        --skip-testpypi-upload)
            SKIP_TESTPYPI_UPLOAD=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-api-tests         Skip testing examples against live API (emergency use only)"
            echo "  --skip-testpypi-upload   Skip uploading to TestPyPI (assumes package already uploaded)"
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

PACKAGE_NAME="balancing-services"
SANDBOX_DIR="/tmp/balancing-services-test-sandbox-$$"

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
echo -e "${BLUE}Test & Publish Pipeline${NC}"
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

if [ "$SKIP_API_TESTS" = false ] && [ -z "$BALANCING_SERVICES_API_KEY" ]; then
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
    if [ "$SKIP_API_TESTS" = false ]; then
        echo "  export BALANCING_SERVICES_API_KEY='your-api-key'"
    fi
    echo "  export UV_PUBLISH_TOKEN_TESTPYPI='your-testpypi-token'"
    echo "  export UV_PUBLISH_TOKEN_PYPI='your-pypi-token'"
    echo ""
    echo "Get your credentials from:"
    if [ "$SKIP_API_TESTS" = false ]; then
        echo "  - API Key: https://balancing.services"
    fi
    echo "  - TestPyPI: https://test.pypi.org/manage/account/token/"
    echo "  - PyPI: https://pypi.org/manage/account/token/"
    echo ""
    if [ "$SKIP_API_TESTS" = false ]; then
        echo "Note: Use --skip-api-tests to skip API testing (emergency use only)"
    fi
    exit 1
fi

# Warn if skipping API tests
if [ "$SKIP_API_TESTS" = true ]; then
    echo -e "${YELLOW}⚠ WARNING: Skipping live API tests${NC}"
    echo -e "${YELLOW}This should only be used in emergencies (e.g., API server is down)${NC}"
    echo -e "${YELLOW}The package will NOT be tested against the live API before publishing!${NC}"
    echo ""
    read -p "Are you sure you want to continue without API testing? (yes/no): " -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo -e "${YELLOW}Publishing cancelled${NC}"
        exit 0
    fi
    echo ""
fi

# Generate pyproject.toml from draft
echo -e "${YELLOW}► Generating pyproject.toml...${NC}"
./generate-pyproject.sh
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

./check.sh

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
# Use --index-url for TestPyPI and --extra-index-url for PyPI (for dependencies)
# Use --index-strategy unsafe-best-match to allow searching both indexes for the package
# Use --no-cache to ensure we get the freshly published version
if ! install_with_retry "uv --no-cache pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --index-strategy unsafe-best-match \"${PACKAGE_NAME}==${VERSION}\""; then
    echo -e "${RED}Error: Failed to install package from TestPyPI${NC}"
    exit 1
fi
echo ""

# Step 5: Run smoke tests using examples
if [ "$SKIP_API_TESTS" = false ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 5: Running Smoke Tests${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    # Return to python client directory to copy examples
    cd "$PYTHON_CLIENT_DIR"

    # Copy examples to sandbox
    echo -e "${YELLOW}► Copying examples to sandbox...${NC}"
    cp -r examples "$SANDBOX_DIR/"
    echo -e "${GREEN}✓ Examples copied${NC}"
    echo ""

    # Return to sandbox
    cd "$SANDBOX_DIR"

    echo -e "${YELLOW}► Running example scripts against live API...${NC}"
    echo ""

    # Run each example (they'll handle auth failures gracefully)
    EXAMPLES=(
        "examples/basic_usage.py"
        "examples/error_handling.py"
        "examples/pagination_example.py"
    )

    for example in "${EXAMPLES[@]}"; do
        if [ -f "$example" ]; then
            example_name=$(basename "$example")
            echo -e "  Testing ${example_name}..."

            # Run the example with API key and capture output
            OUTPUT=$(uv run python "$example" --api-token "$BALANCING_SERVICES_API_KEY" 2>&1)
            EXIT_CODE=$?

            # Check for successful execution (should see "Queried period", "Summary", or similar success indicators)
            if echo "$OUTPUT" | grep -q -E "(Queried period|Summary|successfully)"; then
                echo -e "    ${GREEN}✓${NC} ${example_name} executed successfully"
            elif echo "$OUTPUT" | grep -q -E "(Authentication failed|401)"; then
                echo -e "    ${RED}✗${NC} ${example_name} - Authentication failed"
                echo -e "${RED}Error: API key is invalid or expired${NC}"
                exit 1
            elif [ $EXIT_CODE -ne 0 ]; then
                echo -e "    ${RED}✗${NC} ${example_name} - Script crashed"
                echo -e "${RED}Error: Example script failed to run${NC}"
                echo "$OUTPUT"
                exit 1
            else
                echo -e "    ${YELLOW}⚠${NC} ${example_name} - Unexpected output (may be OK)"
            fi
        else
            echo -e "  ${YELLOW}⚠${NC} ${example} not found, skipping"
        fi
    done

    echo ""
    echo -e "${GREEN}✓ All example smoke tests passed${NC}"
    echo ""
else
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 5: Skipping Smoke Tests${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}⚠ API tests skipped - package not validated against live API${NC}"
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
    echo "  cd clients/python"
    echo "  UV_PUBLISH_TOKEN=\"\$UV_PUBLISH_TOKEN_PYPI\" uv publish"
    exit 0
fi

# Return to python client directory for publishing
cd "$PYTHON_CLIENT_DIR"

echo -e "${YELLOW}► Publishing to PyPI...${NC}"
UV_PUBLISH_TOKEN="$UV_PUBLISH_TOKEN_PYPI" uv publish

echo ""
echo -e "${GREEN}✓ Successfully published to PyPI!${NC}"
echo ""
echo "View at: https://pypi.org/project/${PACKAGE_NAME}/${VERSION}/"
echo ""

# Step 7: Verify PyPI package (only if we ran API tests earlier)
if [ "$SKIP_API_TESTS" = false ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Step 7: Verify PyPI Package${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    echo -e "${YELLOW}► Verifying production PyPI package...${NC}"
    echo ""

    # Create new sandbox for PyPI verification
    PYPI_SANDBOX_DIR="/tmp/balancing-services-pypi-verify-$$"
    mkdir -p "$PYPI_SANDBOX_DIR"
    cd "$PYPI_SANDBOX_DIR"

    echo -e "${YELLOW}► Creating verification environment...${NC}"
    uv venv
    echo -e "${GREEN}✓ Environment created${NC}"
    echo ""

    echo -e "${YELLOW}► Installing ${PACKAGE_NAME} from production PyPI...${NC}"
    # Use --no-cache to ensure we get the freshly published version
    if ! install_with_retry "uv --no-cache pip install \"${PACKAGE_NAME}==${VERSION}\""; then
        echo -e "${RED}Error: Failed to install package from PyPI${NC}"
        exit 1
    fi
    echo ""

    # Copy examples to PyPI sandbox
    cd "$PYTHON_CLIENT_DIR"
    cp -r examples "$PYPI_SANDBOX_DIR/"
    cd "$PYPI_SANDBOX_DIR"

    echo -e "${YELLOW}► Running verification tests against PyPI package...${NC}"
    echo ""

    # Run examples against PyPI package
    EXAMPLES=(
        "examples/basic_usage.py"
        "examples/error_handling.py"
        "examples/pagination_example.py"
    )

    VERIFICATION_FAILED=false
    for example in "${EXAMPLES[@]}"; do
        if [ -f "$example" ]; then
            example_name=$(basename "$example")
            echo -e "  Verifying ${example_name}..."

            OUTPUT=$(uv run python "$example" --api-token "$BALANCING_SERVICES_API_KEY" 2>&1)
            if echo "$OUTPUT" | grep -q -E "(Queried period|Summary|successfully)"; then
                echo -e "    ${GREEN}✓${NC} ${example_name} works with PyPI package"
            else
                echo -e "    ${RED}✗${NC} ${example_name} failed with PyPI package"
                VERIFICATION_FAILED=true
            fi
        fi
    done

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
