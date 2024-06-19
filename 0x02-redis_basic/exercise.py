#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    ''' def count calls with wrapper'''
    @wraps(method)
    def wrapper(self, *args, **kwds):
        ''' def wrapper '''
        name_key = method.__qualname__
        self._redis.incr(name_key, 0) + 1
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    ''' def call history with wrapper'''
    @wraps(method)
    def wrapper(self, *args, **kwds):
        ''' def wrapper'''
        key_method = method.__qualname__
        output_method = key_method + ":outputs"
        input_m = key_method + ':inputs'
        data = str(args)
        self._redis.rpush(input_m, data)
        fin = method(self, *args, **kwds)
        self._redis.rpush(output_method, str(fin))
        return fin
    return wrapper


def replay(func: Callable):
    '''def replay'''
    r = redis.Redis()
    key_method = func.__qualname__
    input_m = r.lrange("{}:inputs".format(key_method), 0, -1)
    output_method = r.lrange("{}:outputs".format(key_method), 0, -1)
    calls_number = len(input_m)
    times_str = 'times'
    if calls_number == 1:
        times_str = 'time'
    fin = '{} was called {} {}:'.format(key_method, calls_number, times_str)
    print(fin)
    for k, v in zip(input_m, output_method):
        fin = '{}(*{}) -> {}'.format(
            key_method,
            k.decode('utf-8'),
            v.decode('utf-8')
        )
        print(fin)


class Cache():
    ''' class cache '''
    def __init__(self):
        ''' def init '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' def store '''
        generated_str_uuid = str(uuid.uuid4())
        self._redis.set(generated_str_uuid, data)
        return generated_str_uuid

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        ''' def get '''
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_int(self, key):
        return self.get(key, int)

    def get_str(self, key):
        value = self._redis.get(key)
        return value.decode("utf-8")
