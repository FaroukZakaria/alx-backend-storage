#!/usr/bin/env python3
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
