"""Lightweight text helpers reserved for future token-budget work."""


def rough_token_count(text: str) -> int:
    """Approximate token count without adding tokenizer dependencies."""
    return max(1, len(text.split())) if text else 0
