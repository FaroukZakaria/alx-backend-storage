#!/usr/bin/python3
"""
Using redis commands exercise
"""
import uuid
from typing import Union, Callable, Optional

import redis


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

    def get(
            self, key: str, fn: Optional[Callable] = None) -> Union[
                str, bytes, int, float]:
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return key
