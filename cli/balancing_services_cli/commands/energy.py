"""Balancing energy subcommands: energy-activated, energy-offered, energy-prices, energy-bids."""

from __future__ import annotations

import logging
from datetime import datetime

import click
from balancing_services.api.default import (
    get_balancing_energy_activated_volumes,
    get_balancing_energy_bids,
    get_balancing_energy_offered_volumes,
    get_balancing_energy_prices,
)
from balancing_services.models import Area, ReserveType

from balancing_services_cli.client_factory import make_client
from balancing_services_cli.flatten import (
    ENERGY_ACTIVATED,
    ENERGY_BIDS,
    ENERGY_OFFERED,
    ENERGY_PRICES,
    flatten_response,
)
from balancing_services_cli.output import format_api_error, write_rows
from balancing_services_cli.pagination import fetch_all_pages, fetch_first_page
from balancing_services_cli.types import ISO8601

log = logging.getLogger(__name__)

AREA_CHOICES = [a.value for a in Area]
RESERVE_TYPE_CHOICES = [r.value for r in ReserveType]


@click.command("energy-activated")
@click.option(
    "--area",
    required=True,
    type=click.Choice(AREA_CHOICES, case_sensitive=False),
    help="Area code.",
)
@click.option("--start", required=True, type=ISO8601, help="Period start (ISO 8601).")
@click.option("--end", required=True, type=ISO8601, help="Period end (ISO 8601).")
@click.option(
    "--reserve-type",
    required=True,
    type=click.Choice(RESERVE_TYPE_CHOICES, case_sensitive=False),
    help="Reserve type.",
)
@click.pass_context
def energy_activated(ctx: click.Context, area: str, start: datetime, end: datetime, reserve_type: str) -> None:
    """Fetch balancing energy activated volumes."""
    client = make_client(ctx)
    log.debug(
        "GET /balancing/energy/activated-volumes area=%s start=%s end=%s reserve_type=%s",
        area, start, end, reserve_type,
    )
    response = get_balancing_energy_activated_volumes.sync_detailed(
        client=client,
        area=Area(area),
        period_start_at=start,
        period_end_at=end,
        reserve_type=ReserveType(reserve_type),
    )
    if response.status_code != 200:
        raise SystemExit(format_api_error(response))
    n_groups = len(response.parsed.data) if response.parsed else 0
    log.debug("Response: HTTP %d, %d group(s)", response.status_code, n_groups)
    rows = flatten_response(response.parsed.data, ENERGY_ACTIVATED)
    log.debug("Flattened to %d row(s)", len(rows))
    write_rows(rows, ctx.obj["output"], ctx.obj["fmt"])


@click.command("energy-offered")
@click.option(
    "--area",
    required=True,
    type=click.Choice(AREA_CHOICES, case_sensitive=False),
    help="Area code.",
)
@click.option("--start", required=True, type=ISO8601, help="Period start (ISO 8601).")
@click.option("--end", required=True, type=ISO8601, help="Period end (ISO 8601).")
@click.option(
    "--reserve-type",
    required=True,
    type=click.Choice(RESERVE_TYPE_CHOICES, case_sensitive=False),
    help="Reserve type.",
)
@click.pass_context
def energy_offered(ctx: click.Context, area: str, start: datetime, end: datetime, reserve_type: str) -> None:
    """Fetch balancing energy offered volumes."""
    client = make_client(ctx)
    log.debug(
        "GET /balancing/energy/offered-volumes area=%s start=%s end=%s reserve_type=%s",
        area, start, end, reserve_type,
    )
    response = get_balancing_energy_offered_volumes.sync_detailed(
        client=client,
        area=Area(area),
        period_start_at=start,
        period_end_at=end,
        reserve_type=ReserveType(reserve_type),
    )
    if response.status_code != 200:
        raise SystemExit(format_api_error(response))
    n_groups = len(response.parsed.data) if response.parsed else 0
    log.debug("Response: HTTP %d, %d group(s)", response.status_code, n_groups)
    rows = flatten_response(response.parsed.data, ENERGY_OFFERED)
    log.debug("Flattened to %d row(s)", len(rows))
    write_rows(rows, ctx.obj["output"], ctx.obj["fmt"])


@click.command("energy-prices")
@click.option(
    "--area",
    required=True,
    type=click.Choice(AREA_CHOICES, case_sensitive=False),
    help="Area code.",
)
@click.option("--start", required=True, type=ISO8601, help="Period start (ISO 8601).")
@click.option("--end", required=True, type=ISO8601, help="Period end (ISO 8601).")
@click.option(
    "--reserve-type",
    required=True,
    type=click.Choice(RESERVE_TYPE_CHOICES, case_sensitive=False),
    help="Reserve type.",
)
@click.pass_context
def energy_prices(ctx: click.Context, area: str, start: datetime, end: datetime, reserve_type: str) -> None:
    """Fetch balancing energy prices."""
    client = make_client(ctx)
    log.debug(
        "GET /balancing/energy/prices area=%s start=%s end=%s reserve_type=%s",
        area, start, end, reserve_type,
    )
    response = get_balancing_energy_prices.sync_detailed(
        client=client,
        area=Area(area),
        period_start_at=start,
        period_end_at=end,
        reserve_type=ReserveType(reserve_type),
    )
    if response.status_code != 200:
        raise SystemExit(format_api_error(response))
    n_groups = len(response.parsed.data) if response.parsed else 0
    log.debug("Response: HTTP %d, %d group(s)", response.status_code, n_groups)
    rows = flatten_response(response.parsed.data, ENERGY_PRICES)
    log.debug("Flattened to %d row(s)", len(rows))
    write_rows(rows, ctx.obj["output"], ctx.obj["fmt"])


@click.command("energy-bids")
@click.option(
    "--area",
    required=True,
    type=click.Choice(AREA_CHOICES, case_sensitive=False),
    help="Area code.",
)
@click.option("--start", required=True, type=ISO8601, help="Period start (ISO 8601).")
@click.option("--end", required=True, type=ISO8601, help="Period end (ISO 8601).")
@click.option(
    "--reserve-type",
    required=True,
    type=click.Choice(RESERVE_TYPE_CHOICES, case_sensitive=False),
    help="Reserve type.",
)
@click.option("--all/--first-page", "fetch_all", default=None, help="Fetch all pages or only the first page.")
@click.pass_context
def energy_bids(
    ctx: click.Context, area: str, start: datetime, end: datetime, reserve_type: str, fetch_all: bool | None,
) -> None:
    """Fetch balancing energy bids."""
    if fetch_all is None:
        raise click.UsageError("You must specify either --all or --first-page.")
    client = make_client(ctx)
    log.debug(
        "GET /balancing/energy/bids area=%s start=%s end=%s reserve_type=%s",
        area, start, end, reserve_type,
    )
    fetch = fetch_all_pages if fetch_all else fetch_first_page
    data = fetch(
        get_balancing_energy_bids.sync_detailed,
        client=client,
        area=Area(area),
        period_start_at=start,
        period_end_at=end,
        reserve_type=ReserveType(reserve_type),
    )
    rows = flatten_response(data, ENERGY_BIDS)
    log.debug("Flattened to %d row(s)", len(rows))
    write_rows(rows, ctx.obj["output"], ctx.obj["fmt"])
