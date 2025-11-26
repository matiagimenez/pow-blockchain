# PoW Miner

The **PoW Miner** is a critical component of the blockchain network, responsible for solving Proof of Work (PoW) challenges. It receives mining tasks from a coordinator node (Block Orchestrator) and uses computational power to find a nonce that satisfies the difficulty target.

## Purpose

The primary purpose of this miner is to secure the blockchain by validating blocks through Proof of Work. It supports both CPU and GPU (CUDA) mining strategies to efficiently solve cryptographic challenges.

## Key Features

- **Hybrid Mining**: Automatically selects between CPU and GPU (CUDA) mining based on availability.
- **Task Consumption**: Listens for mining tasks from a RabbitMQ queue (`tasks`).
- **Block Validation**: Computes the hash of the block header and a nonce until the target difficulty is met.
- **Orchestrator Integration**: Submits solved blocks (with the correct nonce and hash) back to the Block Orchestrator for validation and addition to the blockchain.
- **Keep-Alive**: Sends periodic heartbeat signals to a Pool Manager to indicate active status.

## Help

Run pre-commit over the `pow_miner` files

```sh
pre-commit run --files $(git ls-files ".")
```

Run the HTTP Server

```sh
uvicorn pow_miner.main:main --host 0.0.0.0 --port 8000
```