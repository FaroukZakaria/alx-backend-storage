#!/usr/bin/env python3
"""
Using redis commands exercise
"""
import uuid
from typing import Union, Callable, Optional
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}_calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Append input arguments to Redis list
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to get the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis list
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper

class Cache():
    """
    Cache class
    """
    def __init__(self):
        """
        Initializations
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store random generated ID to instance
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(
            self, key: str, fn: Optional[Callable] = None) -> Union[
                str, bytes, int, float]:
        """
        Get method (callable optional function)
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """
        get string method
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        get integer method
        """
        return self.get(key, fn=int)