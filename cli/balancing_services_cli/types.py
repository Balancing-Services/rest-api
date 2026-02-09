"""Custom Click parameter types."""

from __future__ import annotations

from datetime import datetime

import click
from dateutil.parser import isoparse


class Iso8601Type(click.ParamType):
    """Click parameter type that parses ISO 8601 datetime strings (including Z and +00:00)."""

    name = "ISO8601"

    def convert(self, value: str, param: click.Parameter | None, ctx: click.Context | None) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            return isoparse(value)
        except (ValueError, TypeError):
            self.fail(f"'{value}' is not a valid ISO 8601 datetime.", param, ctx)


ISO8601 = Iso8601Type()
