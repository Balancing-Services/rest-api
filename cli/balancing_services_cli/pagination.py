"""Auto-pagination for bids endpoints."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from balancing_services_cli.output import format_api_error

log = logging.getLogger(__name__)


def fetch_all_pages(
    fetch_fn: Callable[..., Any],
    *,
    verbose: bool = False,
    **kwargs: Any,
) -> list[Any]:
    """Fetch all pages from a paginated endpoint, collecting data items.

    Args:
        fetch_fn: The sync_detailed function to call (e.g. get_balancing_energy_bids.sync_detailed).
        verbose: Unused, kept for backwards compatibility. Use --verbose flag instead.
        **kwargs: Arguments forwarded to fetch_fn (client, area, period_start_at, etc.).

    Returns:
        Combined list of all data items across pages.
    """
    all_data: list[Any] = []
    cursor = None
    page = 1

    while True:
        if cursor is not None:
            kwargs["cursor"] = cursor
        log.debug("Fetching page %d...", page)
        response = fetch_fn(**kwargs)

        if response.status_code != 200:
            raise SystemExit(format_api_error(response))

        parsed = response.parsed
        all_data.extend(parsed.data)
        log.debug("Page %d: got %d group(s), has_more=%s", page, len(parsed.data), parsed.has_more)

        if not parsed.has_more:
            break

        cursor = parsed.next_cursor
        if not cursor:
            break
        page += 1

    log.debug("Fetched %d page(s), %d total group(s)", page, len(all_data))
    return all_data
