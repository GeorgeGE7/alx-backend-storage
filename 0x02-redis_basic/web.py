#!/usr/bin/env python3
import requests
import time
from functools import wraps
from typing import Dict

cache: Dict[str, str] = {}

def get_page(url: str) -> str:
    if url in cache:
        print(f"Retrieving from cache: {url}")
        return cache[url]
    else:
        print(f"Retrieving from web: {url}")
        res = requests.get(url)
        result = res.text
        cache[url] = result
        return result

def cache_with_expiration(expiration: int) -> None:
    def decorator(func) -> None:
        @wraps(func)
        def wrapper(*args, **kwargs):# -> Any | None:
            url = args[0]
            key = f"count:{url}"
            if key in cache:
                count, timestamp = cache[key]
                if time.time() - timestamp > expiration:
                    result = func(*args, **kwargs)
                    cache[key] = (count+1, time.time())
                    return result
                else:
                    cache[key] = (count+1, timestamp)
                    return
