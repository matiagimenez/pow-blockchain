import random


def generate_wallet_address() -> str:
    """Generate a random Ethereum-style wallet address."""
    hex_chars = "0123456789abcdef"
    body = "".join(random.choice(hex_chars) for _ in range(40))
    return f"0x{body}"
