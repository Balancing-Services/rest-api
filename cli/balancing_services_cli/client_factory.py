"""Create an authenticated API client from CLI options."""

from __future__ import annotations

import logging
import sys

import click
from balancing_services import AuthenticatedClient

BASE_URL = "https://api.balancing.services/v1"

log = logging.getLogger(__name__)


def make_client(ctx: click.Context) -> AuthenticatedClient:
    """Build an AuthenticatedClient from the Click context's global options."""
    token: str | None = ctx.obj.get("token")
    if not token:
        click.echo("Error: API token is required. Use --token or set BALANCING_SERVICES_API_KEY.", err=True)
        sys.exit(1)
    log.debug("Creating client for %s", BASE_URL)
    return AuthenticatedClient(base_url=BASE_URL, token=token)
