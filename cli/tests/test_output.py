"""Tests for the output module."""

from __future__ import annotations

import os
import tempfile

from balancing_services_cli.output import detect_format, write_rows


def test_detect_format_explicit():
    assert detect_format("data.csv", "parquet") == "parquet"
    assert detect_format(None, "parquet") == "parquet"


def test_detect_format_by_extension():
    assert detect_format("output.parquet", None) == "parquet"
    assert detect_format("output.csv", None) == "csv"


def test_detect_format_defaults_csv():
    assert detect_format(None, None) == "csv"
    assert detect_format("output.txt", None) == "csv"


def test_write_csv_to_file():
    rows = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        path = f.name
    try:
        write_rows(rows, path, "csv")
        with open(path) as f:
            content = f.read()
        assert "a,b" in content
        assert "1,x" in content
        assert "2,y" in content
    finally:
        os.unlink(path)


def test_write_csv_to_stdout(capsys):
    rows = [{"col": "val"}]
    write_rows(rows, None, "csv")
    captured = capsys.readouterr()
    assert "col" in captured.out
    assert "val" in captured.out



def test_write_empty_csv(capsys):
    write_rows([], None, "csv")
    captured = capsys.readouterr()
    assert captured.out == ""


def test_write_parquet_to_file():
    import pyarrow.parquet as pq

    rows = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
        path = f.name
    try:
        write_rows(rows, path, "parquet")
        table = pq.read_table(path)
        assert table.num_rows == 2
        assert table.column_names == ["a", "b"]
    finally:
        os.unlink(path)


def test_write_parquet_no_output_raises():
    import pytest

    with pytest.raises(SystemExit, match="requires a file path"):
        write_rows([{"a": 1}], None, "parquet")
