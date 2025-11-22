# Block Orchestrator

A small orchestration service that prepares, validates and packages transactions into blocks for a Proof-of-Work (PoW) blockchain network.

Purpose

- Define transaction structure and validation rules used across the network.
- Assemble transactions into candidate blocks and prepare work for miner/worker nodes.

Key Features

- Transaction model: central definitions for transaction format and basic validation logic.
- Block formation: collect and order transactions into block candidates ready for mining.
- Lightweight orchestration: focuses on block assembly and validation, not on mining itself.

### Help

Run pre-commit over the `block_orchestrator` files

```sh
pre-commit run --files $(git ls-files ".")
```

Run the HTTP Server

```sh
uvicorn block_orchestrator.main:main --host 0.0.0.0 --port 8000
```
