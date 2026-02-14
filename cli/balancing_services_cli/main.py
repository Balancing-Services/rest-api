"""CLI entry point and Click group with global options."""

from __future__ import annotations

import logging
import sys

import click

from balancing_services_cli.commands.capacity import (
    capacity_bids,
    capacity_cross_zonal,
    capacity_prices,
    capacity_procured,
)
from balancing_services_cli.commands.energy import (
    energy_activated,
    energy_bids,
    energy_offered,
    energy_prices,
)
from balancing_services_cli.commands.imbalance import (
    imbalance_prices,
    imbalance_volumes,
)


@click.group()
@click.option("--token", help="API bearer token.")
@click.option(
    "--base-url",
    default="https://agents.balancing.services/api/v1",
    show_default=True,
    help="Base URL of the API server.",
)
@click.option("--output", "-o", default=None, help="Output file path (.csv, .parquet, .json).")
@click.option(
    "--format",
    "-f",
    "fmt",
    type=click.Choice(["csv", "parquet"]),
    default=None,
    help="Output format; default: csv (overrides file extension detection).",
)
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print progress messages to stderr.")
@click.pass_context
def cli(
    ctx: click.Context, token: str | None, base_url: str, output: str | None, fmt: str | None, verbose: bool
) -> None:
    """Balancing Services CLI - access European electricity balancing market data."""
    if verbose:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(name)s: %(message)s"))
        pkg_logger = logging.getLogger("balancing_services_cli")
        pkg_logger.setLevel(logging.DEBUG)
        pkg_logger.addHandler(handler)
    ctx.ensure_object(dict)
    ctx.obj["token"] = token
    ctx.obj["base_url"] = base_url
    ctx.obj["output"] = output
    ctx.obj["fmt"] = fmt
    ctx.obj["verbose"] = verbose


cli.add_command(imbalance_prices)
cli.add_command(imbalance_volumes)
cli.add_command(energy_activated)
cli.add_command(energy_offered)
cli.add_command(energy_prices)
cli.add_command(energy_bids)
cli.add_command(capacity_bids)
cli.add_command(capacity_prices)
cli.add_command(capacity_procured)
cli.add_command(capacity_cross_zonal)
