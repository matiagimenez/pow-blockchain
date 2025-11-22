import random
from typing import Any

import requests
from helpers import generate_md5_hash
from utils import Settings, logger


def create_transaction_data() -> dict[str, Any]:
    return {
        "sender": generate_md5_hash(),
        "receiver": generate_md5_hash(),
        "amount": random.randint(1, 10000),
    }


def send_transaction() -> None:
    data = create_transaction_data()
    url = f"{Settings.BLOCK_ORCHESTRATOR_URL}/transaction"

    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        logger.info(f"Transaction sent successfully to {url}. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending transaction: {e}")