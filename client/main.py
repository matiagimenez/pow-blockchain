import time

from helpers import send_transaction
from utils import Settings, logger


def main() -> None:
    logger.info("Starting transaction client...")
    logger.info(f"Block Orchestrator URL: {Settings.BLOCK_ORCHESTRATOR_URL}")
    logger.info(f"Transactions per batch: {Settings.TRANSACTIONS_PER_BATCH}")
    logger.info(f"Batch interval: {Settings.BATCH_INTERVAL_SECONDS} seconds")

    while True:
        for _ in range(Settings.TRANSACTIONS_PER_BATCH):
            send_transaction()
        time.sleep(Settings.BATCH_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
