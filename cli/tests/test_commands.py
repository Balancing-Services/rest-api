"""Tests for CLI commands using Click's test runner."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from unittest.mock import patch
from urllib.error import URLError

from balancing_services.models import Problem
from balancing_services.models.problem_type import ProblemType
from click.testing import CliRunner

from balancing_services_cli.main import cli

# ── Stub API response objects ────────────────────────────────────────────


class StubArea(str, Enum):
    EE = "EE"


class StubDirection(str, Enum):
    POSITIVE = "positive"


class StubCurrency(str, Enum):
    EUR = "EUR"


@dataclass
class StubPeriod:
    start_at: datetime
    end_at: datetime


@dataclass
class StubPriceItem:
    period: StubPeriod
    price: float


@dataclass
class StubImbalancePricesGroup:
    area: Any
    eic_code: str
    currency: Any
    direction: Any
    prices: list[StubPriceItem]


@dataclass
class StubQueriedPeriod:
    start_at: datetime
    end_at: datetime


@dataclass
class StubResponse:
    status_code: int
    parsed: Any = None
    content: bytes = b""


@dataclass
class StubParsedImbalancePrices:
    queried_period: StubQueriedPeriod
    data: list[StubImbalancePricesGroup]
    has_more: bool = False


PERIOD = StubPeriod(
    start_at=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    end_at=datetime(2025, 1, 1, 1, 0, 0, tzinfo=timezone.utc),
)


def _make_imbalance_prices_response():
    return StubResponse(
        status_code=200,
        parsed=StubParsedImbalancePrices(
            queried_period=StubQueriedPeriod(
                start_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                end_at=datetime(2025, 1, 2, tzinfo=timezone.utc),
            ),
            data=[
                StubImbalancePricesGroup(
                    area=StubArea("EE"),
                    eic_code="10X1001A1001A39Y",
                    currency=StubCurrency("EUR"),
                    direction=StubDirection("positive"),
                    prices=[StubPriceItem(period=PERIOD, price=45.5)],
                ),
            ],
        ),
    )


# ── Tests ────────────────────────────────────────────────────────────────


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "imbalance-prices" in result.output
    assert "imbalance-volumes" in result.output
    assert "energy-activated" in result.output
    assert "energy-bids" in result.output
    assert "capacity-bids" in result.output


def test_imbalance_prices_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["imbalance-prices", "--help"])
    assert result.exit_code == 0
    assert "--area" in result.output
    assert "--start" in result.output
    assert "--end" in result.output


def test_imbalance_prices_csv_output():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.imbalance.get_imbalance_prices.sync_detailed",
        return_value=_make_imbalance_prices_response(),
    ):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "imbalance-prices",
                "--area",
                "EE",
                "--start",
                "2025-01-01",
                "--end",
                "2025-01-02",
            ],
        )
    assert result.exit_code == 0
    assert "area" in result.output
    assert "EE" in result.output
    assert "45.5" in result.output


def test_missing_token():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.imbalance.get_imbalance_prices.sync_detailed",
    ) as mock_fn:
        result = runner.invoke(
            cli,
            [
                "imbalance-prices",
                "--area",
                "EE",
                "--start",
                "2025-01-01",
                "--end",
                "2025-01-02",
            ],
        )
    assert result.exit_code != 0
    assert "token" in result.output.lower()
    mock_fn.assert_not_called()


def test_api_error():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.imbalance.get_imbalance_prices.sync_detailed",
        return_value=StubResponse(status_code=401, content=b"Unauthorized"),
    ):
        result = runner.invoke(
            cli,
            [
                "--token",
                "bad-token",
                "imbalance-prices",
                "--area",
                "EE",
                "--start",
                "2025-01-01",
                "--end",
                "2025-01-02",
            ],
        )
    assert result.exit_code != 0


def test_api_error_with_problem_response():
    """When the API returns a Problem object, the CLI should show its title and detail."""
    runner = CliRunner()
    problem = Problem(
        type_=ProblemType.MISSING_PARAMETER,
        title="Missing required parameter",
        status=400,
        detail="Missing required parameter period-start-at.",
    )
    with patch(
        "balancing_services_cli.commands.imbalance.get_imbalance_prices.sync_detailed",
        return_value=StubResponse(status_code=400, parsed=problem),
    ):
        result = runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "imbalance-prices",
                "--area",
                "EE",
                "--start",
                "2025-01-01",
                "--end",
                "2025-01-02",
            ],
        )
    assert result.exit_code != 0
    assert "Missing required parameter" in result.output
    assert "period-start-at" in result.output


def test_naive_datetime_assumed_utc():
    """Dates without timezone info should be treated as UTC when calling the API."""
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.imbalance.get_imbalance_prices.sync_detailed",
        return_value=_make_imbalance_prices_response(),
    ) as mock_fn:
        runner.invoke(
            cli,
            [
                "--token",
                "test-token",
                "imbalance-prices",
                "--area",
                "EE",
                "--start",
                "2025-01-01",
                "--end",
                "2025-01-02",
            ],
        )
    call_kwargs = mock_fn.call_args[1]
    assert call_kwargs["period_start_at"] == datetime(2025, 1, 1, tzinfo=timezone.utc)
    assert call_kwargs["period_end_at"] == datetime(2025, 1, 2, tzinfo=timezone.utc)


BID_COMMANDS = ["energy-bids", "capacity-bids"]
COMMON_BID_ARGS = ["--area", "EE", "--start", "2025-01-01", "--end", "2025-01-02", "--reserve-type", "aFRR"]


@dataclass
class StubBidsParsed:
    data: list[Any]
    has_more: bool = False
    next_cursor: str | None = None


def _make_bids_response():
    return StubResponse(status_code=200, parsed=StubBidsParsed(data=[]))


def test_bids_commands_require_all_or_first_page():
    """energy-bids and capacity-bids must fail without --all or --first-page."""
    runner = CliRunner()
    for cmd in BID_COMMANDS:
        result = runner.invoke(cli, ["--token", "test-token", cmd, *COMMON_BID_ARGS])
        assert result.exit_code != 0, f"{cmd} should fail without --all/--first-page"
        assert "--all" in result.output or "--first-page" in result.output


def test_energy_bids_all_flag():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.energy.get_balancing_energy_bids.sync_detailed",
        return_value=_make_bids_response(),
    ):
        result = runner.invoke(cli, ["--token", "test-token", "energy-bids", "--all", *COMMON_BID_ARGS])
    assert result.exit_code == 0, result.output


def test_energy_bids_first_page_flag():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.energy.get_balancing_energy_bids.sync_detailed",
        return_value=_make_bids_response(),
    ):
        result = runner.invoke(cli, ["--token", "test-token", "energy-bids", "--first-page", *COMMON_BID_ARGS])
    assert result.exit_code == 0, result.output


def test_capacity_bids_all_flag():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.capacity.get_balancing_capacity_bids.sync_detailed",
        return_value=_make_bids_response(),
    ):
        result = runner.invoke(cli, ["--token", "test-token", "capacity-bids", "--all", *COMMON_BID_ARGS])
    assert result.exit_code == 0, result.output


def test_capacity_bids_first_page_flag():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.capacity.get_balancing_capacity_bids.sync_detailed",
        return_value=_make_bids_response(),
    ):
        result = runner.invoke(cli, ["--token", "test-token", "capacity-bids", "--first-page", *COMMON_BID_ARGS])
    assert result.exit_code == 0, result.output


def test_all_subcommands_listed():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    expected = [
        "imbalance-prices",
        "imbalance-volumes",
        "energy-activated",
        "energy-offered",
        "energy-prices",
        "energy-bids",
        "capacity-bids",
        "capacity-prices",
        "capacity-procured",
        "capacity-cross-zonal",
        "check-update",
    ]
    for cmd in expected:
        assert cmd in result.output, f"Missing subcommand: {cmd}"


# ── Version / update tests ───────────────────────────────────────────────


def test_version_flag():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "bs-cli" in result.output
    assert "version" in result.output


def _make_pypi_response(version_str: str) -> bytes:
    return json.dumps({"info": {"version": version_str}}).encode()


def test_check_update_newer_available():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.version.urllib.request.urlopen",
    ) as mock_urlopen:
        mock_urlopen.return_value.__enter__ = lambda s: s
        mock_urlopen.return_value.__exit__ = lambda s, *a: None
        mock_urlopen.return_value.read.return_value = _make_pypi_response("999.0.0")
        result = runner.invoke(cli, ["check-update"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["update_available"] is True
    assert data["latest_version"] == "999.0.0"
    assert "current_version" in data


def test_check_update_up_to_date():
    from balancing_services_cli import __version__

    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.version.urllib.request.urlopen",
    ) as mock_urlopen:
        mock_urlopen.return_value.__enter__ = lambda s: s
        mock_urlopen.return_value.__exit__ = lambda s, *a: None
        mock_urlopen.return_value.read.return_value = _make_pypi_response(__version__)
        result = runner.invoke(cli, ["check-update"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["update_available"] is False
    assert data["current_version"] == __version__
    assert data["latest_version"] == __version__


def test_check_update_network_error():
    runner = CliRunner()
    with patch(
        "balancing_services_cli.commands.version.urllib.request.urlopen",
        side_effect=URLError("Connection refused"),
    ):
        result = runner.invoke(cli, ["check-update"])
    assert result.exit_code == 1
    data = json.loads(result.output)
    assert "error" in data
