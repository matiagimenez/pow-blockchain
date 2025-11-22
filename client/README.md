# Blockchain Transaction Client

A Python client that automatically sends transactions to the blockchain network at configurable intervals to generate blocks.

## Features

- Configurable transaction batching and intervals via environment variables
- Automatic retry logic for failed requests
- Type-safe configuration using Pydantic Settings
- Clean separation of concerns with modular functions

## Configuration

The client uses environment variables for configuration. Create a `.env` file based on the provided example:

```sh
cp .env.example .env
```

Available configuration options:

| Variable                 | Description                              | Default                 |
| ------------------------ | ---------------------------------------- | ----------------------- |
| `BLOCK_ORCHESTRATOR_URL` | Blockchain API endpoint                  | `http://localhost:8000` |
| `TRANSACTIONS_PER_BATCH` | Number of transactions to send per batch | `10`                    |
| `BATCH_INTERVAL_SECONDS` | Time to wait between batches             | `225` (3m 45s)          |

## Installation

1. Create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies using `uv`:

```sh
# Using uv (faster)
uv sync --all-groups
```

## Usage

Run the transaction client:

```sh
python3 main.py
```

The client will start sending transactions in batches according to your configuration.
