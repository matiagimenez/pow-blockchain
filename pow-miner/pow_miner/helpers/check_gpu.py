import subprocess
from contextvars import ContextVar

from pow_miner.utils import logger

gpu_context: ContextVar[bool] = ContextVar("gpu_context", default=False)


def _run_nvidia_smi_check() -> bool:
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
    except FileNotFoundError:
        logger.debug("nvidia-smi not found")
        return False


def initialize_gpu_context() -> None:
    is_available = _run_nvidia_smi_check()
    gpu_context.set(is_available)
