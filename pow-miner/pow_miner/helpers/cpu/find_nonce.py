import hashlib


def find_nonce_with_prefix(
    target_hash_prefix: str,
    base_string: str,
    start_nonce: int,
    end_nonce: int,
) -> tuple[int, str] | None:
    """
    Finds a nonce such that the MD5 hash of (nonce + base_string) starts with target_hash_prefix.
    Searches for the nonce within the range [start_nonce, end_nonce].

    Parameters:
    - target_hash_prefix: Prefix of the target hash.
    - base_string: Base string to which the nonce will be concatenated.
    - start_nonce: Start of the nonce range.
    - end_nonce: End of the nonce range.

    Returns:
    - (nonce, hash): The found nonce and the corresponding hash.
    - None: If no nonce meeting the condition is found.
    """
    for nonce in range(start_nonce, end_nonce + 1):
        test_string = f"{nonce}{base_string}"
        hash_ = hashlib.md5(test_string.encode()).hexdigest()  # nosec
        if hash_.startswith(target_hash_prefix):
            return nonce, hash_
    return None


def find_nonce(
    target_hash_prefix: str,
    base_string: str,
    start_nonce: int,
    end_nonce: int,
) -> str:
    result = find_nonce_with_prefix(
        target_hash_prefix=target_hash_prefix,
        base_string=base_string,
        start_nonce=start_nonce,
        end_nonce=end_nonce,
    )

    if not result:
        return "No nonce found that satisfies the condition in the provided range."
    nonce, hash_ = result
    return f"Nonce found: {nonce}\nHash: {hash_}"
