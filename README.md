# PoW Blockchain

A distributed Proof-of-Work blockchain implementation designed for horizontal scalability using modern cloud-native technologies. This project demonstrates how to parallelize and distribute block generation while maintaining blockchain consistency through centralized processing.

## 🚀 Features

- **Distributed Architecture**: Horizontally scalable design supporting multiple mining nodes
- **GPU-Accelerated Mining**: CUDA-based PoW implementation for efficient hash computation
- **Asynchronous Processing**: RabbitMQ-based message queue for transaction and block distribution
- **Container Orchestration**: Full Kubernetes deployment configuration with Docker Compose for local development
- **Infrastructure as Code**: Terraform configuration for GCP deployment
- **Modern Python Stack**: Built with FastAPI, Pydantic, and type-safe configurations

## 📋 Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Components](#components)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Project Structure](#project-structure)

## Introduction

A blockchain is a distributed database where nodes interact in a decentralized peer-to-peer manner to maintain a consistent, immutable ledger of records across the network. In a Proof-of-Work (PoW) architecture, consensus and data integrity are guaranteed through a computationally intensive mining process.

![Blockchain Concept](https://github.com/matiasgimenezdev/pow-blockchain/assets/117539520/fd46df80-1b4a-4091-b0e2-58efedfdac13)

### Distributed Systems Approach

This implementation leverages distributed system principles to achieve horizontal scalability:

- **Multi-Node Architecture**: Supports multiple miners and orchestrators working in parallel
- **Asynchronous Processing**: Message-driven architecture using RabbitMQ for loose coupling
- **Stateless Components**: Redis-backed state management for resilient operation
- **Cloud-Native Design**: Kubernetes-ready with auto-scaling capabilities

### Blockchain Structure

At its core, a blockchain maintains a continuously growing list of ordered records (blocks), similar to an append-only transaction log. Each block contains:

- **Transaction Data**: A collection of validated transactions
- **Previous Block Hash**: Cryptographic link to the parent block
- **Nonce**: The solution to the PoW challenge
- **Timestamp**: Block creation time

![Blockchain Structure](https://github.com/matiasgimenezdev/pow-blockchain/assets/117539520/76aaecac-0942-4733-848d-aa4c080a3736)

While blocks must be processed sequentially to maintain chain integrity, this architecture parallelizes block **generation** across multiple miners. The key insight: if operations are not mutually exclusive or sequential, they can be performed concurrently, dramatically improving throughput.

## Architecture

### System Design [(Interactive Diagram)](https://miro.com/app/board/uXjVK9Am-aU=/?share_link_id=894524781583)

![System Architecture](https://github.com/matiasgimenezdev/pow-blockchain/assets/117539520/2d286bef-23de-43a4-81a5-5a3654c88f0e)

### Component Interaction Flow

1. **Transaction Submission**: Client sends transactions to the Block Orchestrator
2. **Transaction Pooling**: Orchestrator aggregates transactions and publishes to RabbitMQ
3. **Block Generation**: Pool Manager collects transactions and distributes mining tasks
4. **PoW Mining**: Multiple PoW Miners compete to find valid nonces (GPU-accelerated)
5. **Block Validation**: First valid block is accepted and broadcast
6. **Chain Update**: Blockchain state updated in Redis

## Components

### 🎯 Block Orchestrator

The central API service managing transaction intake and block coordination.

- **Technology**: FastAPI, Pydantic Settings
- **Responsibilities**:
  - REST API for transaction submission
  - Transaction validation and queuing
  - Block state management
  - RabbitMQ message publishing
- **Location**: `block-orchestrator`

### 🏊 Pool Manager

Manages the transaction pool and coordinates block generation.

- **Technology**: Python with RabbitMQ consumer
- **Responsibilities**:
  - Transaction pool aggregation
  - Block template creation
  - Mining task distribution
  - Instance computation scheduling
- **Location**: `pool-manager`

### ⛏️ PoW Miner

GPU-accelerated mining worker that solves the Proof-of-Work challenge.

- **Technology**: Python + CUDA (C++)
- **Responsibilities**:
  - Receive mining tasks from queue
  - GPU-based nonce computation (MD5 hashing)
  - Submit valid blocks
  - Automatic task scheduling
- **Location**: `pow-miner`
- **GPU Support**: CUDA kernels for parallel hash computation

### 📤 Transaction Client

Automated client for generating test transactions.

- **Responsibilities**:
  - Generate random transactions
  - Configurable batch sending
  - Environment-based configuration
- **Location**: `client`

## Getting Started

### Prerequisites

- **Python 3.12+**
- **Docker & Docker Compose**
- **CUDA Toolkit** (for GPU mining)
- **Kubernetes** (optional, for production deployment)
- **Terraform** (optional, for cloud infrastructure)

### Local Development with Docker Compose

1. **Start the infrastructure services**:

```bash
docker-compose up -d
```

This starts RabbitMQ, Redis, and other dependencies.

2. **Run individual components**:

Each component has its own README with detailed setup instructions:

- [Block Orchestrator Setup](./block-orchestrator/README.md)
- [Pool Manager Setup](./pool-manager/README.md)
- [PoW Miner Setup](./pow-miner/README.md)
- [Transaction Client Setup](./client/README.md)

### Quick Start Script

```bash
# Build all components
./build.sh

# Or start everything with Docker Compose
docker-compose -f docker-compose.yml up
```

## Deployment

### Kubernetes

Deploy to a Kubernetes cluster using the provided manifests:

```bash
# Apply namespaces
kubectl apply -f kubernetes/namespaces.yml

# Deploy services
kubectl apply -f kubernetes/services/

# Deploy applications
kubectl apply -f kubernetes/applications/
```

See [kubernetes/](./kubernetes/) for detailed configuration.

### Google Cloud Platform with Terraform

Provision infrastructure on GCP:

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

The Terraform configuration includes:

- GKE cluster setup
- VPC networking
- Node pools with GPU support
- Firewall rules

See [terraform/README.md](./terraform/README.md) for details.

## Technology Stack

- **Languages**: Python 3.12+, CUDA C++
- **Frameworks**: FastAPI, Pydantic
- **Message Queue**: RabbitMQ
- **Cache/State**: Redis
- **Container**: Docker, Kubernetes
- **Cloud**: Google Cloud Platform
- **IaC**: Terraform
- **CI/CD**: GitHub Actions (if configured)

## Configuration

All components use environment-based configuration with Pydantic Settings. See individual component READMEs for specific configuration options.

## Contributing

This is an educational/prototype project. Contributions, issues, and feature requests are welcome!

## License

This project is for educational purposes. See individual component licenses if applicable.
