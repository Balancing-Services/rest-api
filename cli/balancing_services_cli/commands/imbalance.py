"""Imbalance subcommands: imbalance-prices, imbalance-volumes."""

from __future__ import annotations

import logging
from datetime import datetime

import click
from balancing_services.api.default import get_imbalance_prices, get_imbalance_total_volumes
from balancing_services.models import Area

from balancing_services_cli.client_factory import make_client
from balancing_services_cli.flatten import IMBALANCE_PRICES, IMBALANCE_VOLUMES, flatten_response
from balancing_services_cli.output import write_rows
from balancing_services_cli.types import ISO8601

log = logging.getLogger(__name__)

AREA_CHOICES = [a.value for a in Area]


@click.command("imbalance-prices")
@click.option(
    "--area",
    required=True,
    type=click.Choice(AREA_CHOICES, case_sensitive=False),
    help="Area code.",
)
@click.option("--start", required=True, type=ISO8601, help="Period start (ISO 8601).")
@click.option("--end", required=True, type=ISO8601, help="Period end (ISO 8601).")
@click.pass_context
def imbalance_prices(ctx: click.Context, area: str, start: datetime, end: datetime) -> None:
    """Fetch imbalance prices."""
    client = make_client(ctx)
    log.debug("GET /imbalance/prices area=%s start=%s end=%s", area, start, end)
    response = get_imbalance_prices.sync_detailed(
        client=client,
        area=Area(area),
        period_start_at=start,
        period_end_at=end,
    )
    n_groups = len(response.parsed.data) if response.parsed else 0
    log.debug("Response: HTTP %d, %d group(s)", response.status_code, n_groups)
    if response.status_code != 200:
        raise SystemExit(f"API error (HTTP {response.status_code}): {response.content.decode()}")
    rows = flatten_response(response.parsed.data, IMBALANCE_PRICES)
    log.debug("Flattened to %d row(s)", len(rows))
    write_rows(rows, ctx.obj["output"], ctx.obj["fmt"])


@click.command("imbalance-volumes")
@click.option(
    "--area",
    required=True,
    type=click.Choice(AREA_CHOICES, case_sensitive=False),
    help="Area code.",
)
@click.option("--start", required=True, type=ISO8601, help="Period start (ISO 8601).")
@click.option("--end", required=True, type=ISO8601, help="Period end (ISO 8601).")
@click.pass_context
def imbalance_volumes(ctx: click.Context, area: str, start: datetime, end: datetime) -> None:
    """Fetch imbalance total volumes."""
    client = make_client(ctx)
    log.debug("GET /imbalance/total-volumes area=%s start=%s end=%s", area, start, end)
    response = get_imbalance_total_volumes.sync_detailed(
        client=client,
        area=Area(area),
        period_start_at=start,
        period_end_at=end,
    )
    n_groups = len(response.parsed.data) if response.parsed else 0
    log.debug("Response: HTTP %d, %d group(s)", response.status_code, n_groups)
    if response.status_code != 200:
        raise SystemExit(f"API error (HTTP {response.status_code}): {response.content.decode()}")
    rows = flatten_response(response.parsed.data, IMBALANCE_VOLUMES)
    log.debug("Flattened to %d row(s)", len(rows))
    write_rows(rows, ctx.obj["output"], ctx.obj["fmt"])
