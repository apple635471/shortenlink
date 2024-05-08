"""core library for shortening URLs"""

import random
import string

CHARSET = string.digits + string.ascii_lowercase + string.ascii_uppercase


def _base62_encode(num: int) -> str:
    """Encode a positive number in base62"""
    if num == 0:
        return "0"
    base62: list[str] = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(CHARSET[rem])
    return "".join(reversed(base62))


def _hashgen(length: int) -> str:
    """Generate a hash"""
    return "".join(random.choices(CHARSET, k=length))


def shorten_url(num: int) -> str:
    """Shorten a URL"""
    return _hashgen(4) + _base62_encode(num)
