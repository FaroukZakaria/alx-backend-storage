#!/usr/bin/python3
"""
Using redis commands exercise
"""
import uuid
import redis
from typing import Union


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
    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store random generated ID to instance
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
    
# Example usage:
cache_instance = Cache()
key = cache_instance.store("Hello, Redis!")
print("Stored key:", key)