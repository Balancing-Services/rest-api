"""Create an authenticated API client from CLI options."""

from __future__ import annotations

import logging
import sys

import click
from balancing_services import AuthenticatedClient

log = logging.getLogger(__name__)


def make_client(ctx: click.Context) -> AuthenticatedClient:
    """Build an AuthenticatedClient from the Click context's global options."""
    token: str | None = ctx.obj.get("token")
    if not token:
        click.echo("Error: API token is required. Use --token.", err=True)
        sys.exit(1)
    base_url: str = ctx.obj["base_url"]
    log.debug("Creating client for %s", base_url)
    return AuthenticatedClient(base_url=base_url, token=token)
