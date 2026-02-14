# balancing-services-cli

Command-line interface for the [Balancing Services REST API](https://balancing.services) - access European electricity balancing market data directly from your terminal.

## Installation

```bash
uv add balancing-services-cli
```

Or with pip:

```bash
pip install balancing-services-cli
```

Or run without installing via `uvx`:

```bash
uvx balancing-services-cli imbalance-prices --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z
```

## Authentication

Provide your API token via the `--token` option:

```bash
bs-cli --token your-token-here imbalance-prices --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z
```

## Usage

```bash
# CSV to stdout (default)
bs-cli imbalance-prices --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z

# Save to CSV file
bs-cli imbalance-prices --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z -o prices.csv

# Save to Parquet
bs-cli imbalance-prices --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z -o prices.parquet

# Balancing energy commands (require --reserve-type)
bs-cli energy-prices --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z --reserve-type aFRR
bs-cli energy-bids --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z --reserve-type mFRR

# Balancing capacity commands (require --reserve-type)
bs-cli capacity-prices --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z --reserve-type aFRR
bs-cli capacity-bids --area EE --start 2025-01-01T00:00:00Z --end 2025-01-02T00:00:00Z --reserve-type FCR
```

## Commands

| Command | Description |
|---|---|
| `imbalance-prices` | Imbalance prices |
| `imbalance-volumes` | Imbalance total volumes |
| `energy-activated` | Balancing energy activated volumes |
| `energy-offered` | Balancing energy offered volumes |
| `energy-prices` | Balancing energy prices |
| `energy-bids` | Balancing energy bids (auto-paginates) |
| `capacity-bids` | Balancing capacity bids (auto-paginates) |
| `capacity-prices` | Balancing capacity prices |
| `capacity-procured` | Balancing capacity procured volumes |
| `capacity-cross-zonal` | Cross-zonal capacity allocation |

## Output Formats

- **CSV** (default): Written to stdout or file. Use with Excel, DuckDB, Polars, pandas, etc.
- **Parquet**: Must specify `-o file.parquet`.


## Global Options

| Option | Description |
|---|---|
| `--token` | API bearer token |
| `-o, --output` | Output file path (auto-detects format from `.csv`/`.parquet` extension) |
| `-f, --format` | Override output format (`csv`, `parquet`) |
