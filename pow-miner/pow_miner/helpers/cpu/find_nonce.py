import hashlib
from typing import Any


def find_nonce(
    target_hash_prefix: str,
    base_string: str,
    start_nonce: int,
    end_nonce: int,
) -> dict[str, Any]:
    """
    Finds a nonce such that the MD5 hash of (nonce + base_string) starts with target_hash_prefix.
    Searches for the nonce within the range [start_nonce, end_nonce].

    Parameters:
    - target_hash_prefix: Prefix of the target hash.
    - base_string: Base string to which the nonce will be concatenated.
    - start_nonce: Start of the nonce range.
    - end_nonce: End of the nonce range.
    """
    for nonce in range(start_nonce, end_nonce + 1):
        test_string = f"{nonce}{base_string}"
        hash_ = hashlib.md5(test_string.encode()).hexdigest()  # nosec
        if hash_.startswith(target_hash_prefix):
            return {"nonce": nonce, "hash": hash_}
    return {}
