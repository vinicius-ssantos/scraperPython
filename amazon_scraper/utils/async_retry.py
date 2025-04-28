# utils/async_retry.py
import asyncio
from functools import wraps


def async_retry(retries=3, base_delay=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        raise
                    await asyncio.sleep(base_delay * (2 ** (attempt - 1)))
        return wrapper
    return decorator
