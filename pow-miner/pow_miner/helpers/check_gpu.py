import subprocess

from pow_miner.utils import logger


def check_for_nvidia_smi() -> bool:
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logger.info(result.stdout.decode("utf-8"))
        return True
    except subprocess.CalledProcessError as e:
        logger.debug(f"nvidia-smi failed with error: {e}")
        return False
