"""
Test that code examples in README.md actually execute without errors.

This test extracts Python code blocks from README and executes them with mocked HTTP responses.
"""

import re
from pathlib import Path

import pytest
import respx
from httpx import Response

# Hardcoded list of examples we have tests for
# If you add a new example to README, add it here and create a test for it
COVERED_EXAMPLES = {
    "Quick Start",
    "Get Balancing Energy Bids with Pagination",
    "Async Usage",
    "Error Handling",
}


def extract_python_code_blocks(readme_path: Path) -> dict[str, str]:
    """Extract Python code blocks from README markdown file."""
    content = readme_path.read_text()

    # Find all Python code blocks with their preceding context
    pattern = r'###?\s+([^\n]+)\n+```python\n(.*?)\n```'
    matches = re.finditer(pattern, content, re.DOTALL)

    blocks = {}
    for match in matches:
        title = match.group(1).strip()
        code = match.group(2)
        # Skip blocks that are just comments or configuration
        if code.strip() and 'get_' in code:
            blocks[title] = code

    return blocks


@pytest.fixture
def mock_success_response():
    """Mock successful API response."""
    return {
        "queriedPeriod": {
            "startAt": "2025-01-01T00:00:00Z",
            "endAt": "2025-01-02T00:00:00Z"
        },
        "hasMore": False,
        "data": [
            {
                "area": "EE",
                "eicCode": "10Y1001A1001A39I",
                "direction": "positive",
                "currency": "EUR",
                "prices": [
                    {
                        "period": {
                            "startAt": "2025-01-01T00:00:00Z",
                            "endAt": "2025-01-01T01:00:00Z"
                        },
                        "price": 45.5
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_bids_response():
    """Mock balancing energy bids response with pagination."""
    return {
        "queriedPeriod": {
            "startAt": "2025-01-01T00:00:00Z",
            "endAt": "2025-01-02T00:00:00Z"
        },
        "hasMore": True,
        "nextCursor": "v1:test_cursor",
        "data": [
            {
                "area": "EE",
                "eicCode": "10Y1001A1001A39I",
                "reserveType": "aFRR",
                "direction": "up",
                "standardProduct": "15MIN",
                "currency": "EUR",
                "bids": [
                    {
                        "period": {
                            "startAt": "2025-01-01T00:00:00Z",
                            "endAt": "2025-01-01T00:15:00Z"
                        },
                        "volume": 10.5,
                        "price": 25.0,
                        "status": "accepted"
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_error_401():
    """Mock 401 unauthorized error response."""
    return {
        "type": "unauthorized",
        "title": "Unauthorized",
        "status": 401,
        "detail": "Invalid API key"
    }


@respx.mock
def test_quick_start_example_executes(mock_success_response):
    """Test that Quick Start example from README executes without errors."""
    # Mock the API endpoint
    respx.get("https://api.balancing.services/v1/imbalance/prices").mock(
        return_value=Response(200, json=mock_success_response)
    )

    readme_path = Path(__file__).parent.parent / "README.md"
    code_blocks = extract_python_code_blocks(readme_path)

    # Find the Quick Start example
    quick_start = code_blocks.get("Quick Start")
    assert quick_start is not None, "Quick Start example not found in README"

    # Execute the code
    exec_globals = {}
    try:
        exec(quick_start, exec_globals)
    except Exception as e:
        pytest.fail(f"Quick Start example failed to execute: {e}\n\nCode:\n{quick_start}")


@respx.mock
def test_pagination_example_executes(mock_bids_response):
    """Test that Pagination example from README executes without errors."""
    # Mock the API endpoint
    respx.get("https://api.balancing.services/v1/balancing/energy/bids").mock(
        return_value=Response(200, json=mock_bids_response)
    )

    readme_path = Path(__file__).parent.parent / "README.md"
    code_blocks = extract_python_code_blocks(readme_path)

    # Find the Pagination example
    pagination = code_blocks.get("Get Balancing Energy Bids with Pagination")
    assert pagination is not None, "Pagination example not found in README"

    # Execute the code
    exec_globals = {}
    try:
        exec(pagination, exec_globals)
    except Exception as e:
        pytest.fail(f"Pagination example failed to execute: {e}\n\nCode:\n{pagination}")


@pytest.mark.asyncio
@respx.mock
async def test_async_example_executes(mock_success_response):
    """Test that Async Usage example from README executes without errors."""
    # Mock the API endpoint
    respx.get("https://api.balancing.services/v1/imbalance/prices").mock(
        return_value=Response(200, json=mock_success_response)
    )

    readme_path = Path(__file__).parent.parent / "README.md"
    code_blocks = extract_python_code_blocks(readme_path)

    # Find the Async example
    async_example = code_blocks.get("Async Usage")
    assert async_example is not None, "Async Usage example not found in README"

    # Execute the async function definition and call it directly
    # (instead of using asyncio.run which doesn't work in test context)
    exec_globals = {}
    try:
        # Remove the asyncio.run() line since we're already in async context
        code_without_run = async_example.rsplit('# Run async function', 1)[0]
        exec(code_without_run, exec_globals)

        # Now call the async function directly
        fetch_prices = exec_globals.get('fetch_prices')
        if fetch_prices:
            await fetch_prices()
    except Exception as e:
        pytest.fail(f"Async Usage example failed to execute: {e}\n\nCode:\n{async_example}")


@respx.mock
def test_error_handling_example_executes(mock_error_401):
    """Test that Error Handling example from README executes without errors."""
    # Mock the API endpoint to return 401
    respx.get("https://api.balancing.services/v1/imbalance/prices").mock(
        return_value=Response(401, json=mock_error_401)
    )

    readme_path = Path(__file__).parent.parent / "README.md"
    code_blocks = extract_python_code_blocks(readme_path)

    # Find the Error Handling example
    error_handling = code_blocks.get("Error Handling")
    assert error_handling is not None, "Error Handling example not found in README"

    # Execute the code
    exec_globals = {}
    try:
        exec(error_handling, exec_globals)
    except Exception as e:
        pytest.fail(f"Error Handling example failed to execute: {e}\n\nCode:\n{error_handling}")


@respx.mock
def test_old_string_based_approach_fails():
    """Test that old approach with strings would fail (validates our fix)."""
    # Mock the API endpoint
    respx.get("https://api.balancing.services/v1/imbalance/prices").mock(
        return_value=Response(200, json={})
    )

    # Old broken code with strings
    old_broken_code = """
from balancing_services import AuthenticatedClient
from balancing_services.api.default import get_imbalance_prices

client = AuthenticatedClient(
    base_url="https://api.balancing.services/v1",
    token="test"
)

# This should fail because area should be Area.EE not "EE"
response = get_imbalance_prices.sync_detailed(
    client=client,
    area="EE",  # Wrong: string instead of Area enum
    period_start_at="2025-01-01T00:00:00Z",  # Wrong: string instead of datetime
    period_end_at="2025-01-02T00:00:00Z"
)
"""

    # This should raise an AttributeError
    with pytest.raises(AttributeError, match="'str' object has no attribute 'value'"):
        exec(old_broken_code, {})


def test_all_readme_examples_are_tested():
    """
    Test that all Python code examples in README have corresponding tests.

    If this test fails, it means:
    1. A new example was added to README without a test, OR
    2. An example was removed from README but is still in COVERED_EXAMPLES

    To fix:
    - Add the new example title to COVERED_EXAMPLES constant
    - Create a test function for the new example
    - OR remove the example from COVERED_EXAMPLES if it was removed from README
    """
    readme_path = Path(__file__).parent.parent / "README.md"
    code_blocks = extract_python_code_blocks(readme_path)

    readme_examples = set(code_blocks.keys())

    # Check for examples in README that aren't covered by tests
    uncovered = readme_examples - COVERED_EXAMPLES
    if uncovered:
        pytest.fail(
            f"Found {len(uncovered)} example(s) in README without tests:\n"
            f"  {', '.join(sorted(uncovered))}\n\n"
            f"Please add these examples to COVERED_EXAMPLES and create tests for them."
        )

    # Check for examples in COVERED_EXAMPLES that aren't in README (stale tests)
    extra = COVERED_EXAMPLES - readme_examples
    if extra:
        pytest.fail(
            f"Found {len(extra)} example(s) in COVERED_EXAMPLES that aren't in README:\n"
            f"  {', '.join(sorted(extra))}\n\n"
            f"These examples may have been removed or renamed. "
            f"Please remove them from COVERED_EXAMPLES."
        )
