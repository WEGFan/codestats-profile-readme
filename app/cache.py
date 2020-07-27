# -*- coding: utf-8 -*-
from typing import Optional

from flask_caching import Cache
from flask_caching.backends import RedisCache

cache = Cache()


def get_key_with_prefix(key: str, prefix: Optional[str]):
    if not prefix:
        return key
    return f'{prefix}/{key}'


def set_redis_expire_seconds(key: str, expire: int):
    if not isinstance(cache.cache, RedisCache):
        return
    cache.cache._write_client.expire(name=cache.cache._get_prefix() + key, time=expire)
