#!/usr/bin/env python3

import requests
import redis
from functools import wraps
import time


def cache_result(expiration_time):
    """
    result
    """
    def decorator(func):
        """
        decorator
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            wrapper
            """
            url = args[0]
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Check if the result is already in the cache
            cached_result = redis_client.get(cache_key)
            if cached_result is not None:
                # Increment the access count
                redis_client.incr(count_key)
                return cached_result.decode("utf-8")

            # If not in the cache, fetch the result
            result = func(*args, **kwargs)

            # Cache the result with expiration time
            redis_client.setex(cache_key, expiration_time, result)

            # Increment the access count
            redis_client.incr(count_key)

            return result
        return wrapper
    return decorator


@cache_result(expiration_time=10)
def get_page(url: str) -> str:
    """
    get page
    """
    response = requests.get(url)
    return response.text


# Initialize Redis client
redis_client = redis.Redis()
