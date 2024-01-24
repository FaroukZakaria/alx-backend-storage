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

# Test the get_page function
slow_url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.google.com"
for _ in range(5):
    content = get_page(slow_url)
    print(content)
    time.sleep(2)  # Introducing a delay to see caching in action

# Print access count for the slow URL
access_count = redis_client.get(f"count:{slow_url}")
print(f"Access count for {slow_url}: {int(access_count)}")
