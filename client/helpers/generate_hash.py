import hashlib
import random


def generate_md5_hash() -> str:
    """Generate a random MD5 hash for transaction identifiers."""
    random_string = "".join(
        random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        for _ in range(16)
    )
    return hashlib.md5(random_string.encode()).hexdigest()
