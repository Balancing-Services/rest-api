"""Write flattened rows to CSV or Parquet."""

from __future__ import annotations

import csv
import io
import logging
import sys
from typing import Any

from balancing_services.models import Problem

log = logging.getLogger(__name__)


def format_api_error(response: Any) -> str:
    """Format a user-friendly error message from an API error response."""
    parsed = response.parsed
    if isinstance(parsed, Problem):
        detail = f": {parsed.detail}" if isinstance(parsed.detail, str) else ""
        return f"API error (HTTP {parsed.status}): {parsed.title}{detail}"
    return f"API error (HTTP {response.status_code}): {response.content.decode()}"


def detect_format(output: str | None, fmt: str | None) -> str:
    """Determine the output format from explicit flag or file extension."""
    if fmt:
        return fmt
    if output and output.endswith(".parquet"):
        return "parquet"
    return "csv"


def write_rows(rows: list[dict[str, Any]], output: str | None, fmt: str | None) -> None:
    """Write rows to the appropriate destination and format."""
    resolved = detect_format(output, fmt)
    dest = output or "stdout"
    log.debug("Writing %d row(s) as %s to %s", len(rows), resolved, dest)
    if resolved == "parquet":
        _write_parquet(rows, output)
    else:
        _write_csv(rows, output)


def _write_csv(rows: list[dict[str, Any]], output: str | None) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    if output:
        with open(output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        sys.stdout.write(buf.getvalue())


def _write_parquet(rows: list[dict[str, Any]], output: str | None) -> None:
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError:
        raise SystemExit(
            "Parquet support requires the 'pyarrow' package.\n"
            "\n"
            "Install it with:\n"
            "  pip install balancing-services-cli[parquet]\n"
            "\n"
            "Or, if using uv:\n"
            "  uv add balancing-services-cli[parquet]"
        )

    if not rows:
        return
    if not output:
        raise SystemExit("Parquet output requires a file path. Use --output/-o to specify a file.")
    table = pa.Table.from_pylist(rows)
    pq.write_table(table, output)
