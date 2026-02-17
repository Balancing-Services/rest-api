"""Check-update command that queries PyPI for the latest CLI version."""

from __future__ import annotations

import json
import urllib.request
from urllib.error import URLError

import click
from packaging.version import Version

from balancing_services_cli import __version__

PYPI_URL = "https://pypi.org/pypi/balancing-services-cli/json"


@click.command("check-update")
def check_update() -> None:
    """Check if a newer CLI version is available on PyPI."""
    try:
        req = urllib.request.Request(PYPI_URL, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        latest = data["info"]["version"]
    except (URLError, OSError, KeyError, json.JSONDecodeError) as exc:
        click.echo(json.dumps({"error": str(exc)}))
        raise SystemExit(1) from None

    click.echo(
        json.dumps(
            {
                "current_version": __version__,
                "latest_version": latest,
                "update_available": Version(latest) > Version(__version__),
            }
        )
    )
