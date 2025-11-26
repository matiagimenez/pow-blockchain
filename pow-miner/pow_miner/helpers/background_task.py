# import json

# import requests

# from pow_miner.utils import Settings, logger

# from .check_gpu import gpu_context


def send_keep_alive() -> None:
    pass
    # external_ip = requests.get("https://checkip.amazonaws.com").text.strip()
    # status = {
    #     "address": external_ip,
    #     "machine_type": "GPU" if gpu_context.get() else "CPU",
    # }

    # url = f"{Settings.POOL_MANAGER_URL}/keep-alive"
    # logger.info(f"Sending keep alive to {url}")
    # requests.post(url, json.dumps(status))
