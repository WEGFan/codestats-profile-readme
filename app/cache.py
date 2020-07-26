# -*- coding: utf-8 -*-
from typing import Optional

from flask_caching import Cache

cache = Cache()


def get_key_with_prefix(key: str, prefix: Optional[str]):
    if not prefix:
        return key
    return f'{prefix}/{key}'
