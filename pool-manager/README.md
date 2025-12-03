# Mining pool Manager

The pool manager acts as an orchestration layer between the block coordinator and distributed mining workers. It optimizes proof-of-work computation by intelligently distributing workload and managing mining resources.

## Responsibilities

- **Task Distribution**: Receives mining tasks from the block orchestrator and partitions the nonce search space into parallelizable subtasks for miner workers.
- **Worker Health Monitoring**: Tracks active GPU miners through periodic keep-alive signals to maintain an accurate view of available mining capacity.
- **Dynamic Resource Scaling**: Automatically provisions and terminates cloud-based CPU miner instances based on workload demand and mining pool utilization.
- **Workload Coordination**: Manages the assignment and reassignment of nonce ranges to ensure efficient mining operations and avoid duplicate work.
