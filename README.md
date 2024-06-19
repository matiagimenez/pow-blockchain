![sdypp grupo 1](https://github.com/matiasgimenezdev/pow-blockchain/assets/117539520/4962a098-5393-4c6d-bcdc-477619690d84)# POW Blockchain

## Introduction

A blockchain is a distributed database where a set of nodes interact in decentralized mode (p2p) to store a set of consistent records between each of the nodes.

The consistency of such information, in a PoW (Proof of Work) architecture, is guaranteed by a process called mining, which, due to its complexity, usually runs on the GPU.

![image](https://github.com/matiasgimenezdev/pow-blockchain/assets/117539520/fd46df80-1b4a-4091-b0e2-58efedfdac13)

To support blockchain developments, you will use distributed system services. This is the answer to the need for horizontal scalability.

-   Inherent to the existence of a distributed system is the existence of two or more nodes.
-   At the core of a distributed system is asynchronous processing.

### Structure of the blockchain

The basic concept of blockchain is quite simple: a database that maintains a continuously growing list of sorted records. Something very similar to a database transaction log.

As can be seen in the image, there is an order and sequentiality in the operations that are recorded in a blockchain, so that, although the content of each block can be generated in a distributed manner, its processing must be centralized. The objective of this project is to present a prototype architecture that allows to parallelize and distribute the generation of blocks.

The main advantage of this architecture is that, if two operations are not mutually exclusive or sequential, they can be performed in parallel.

![image](https://github.com/matiasgimenezdev/pow-blockchain/assets/117539520/76aaecac-0942-4733-848d-aa4c080a3736)

### Designed architecture [URL](https://miro.com/app/board/uXjVK9Am-aU=/?share_link_id=894524781583)

![Blockchain](https://github.com/matiasgimenezdev/pow-blockchain/assets/117539520/2d286bef-23de-43a4-81a5-5a3654c88f0e)
