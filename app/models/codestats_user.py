# -*- coding: utf-8 -*-
import time
from typing import List

import arrow
import requests
from flask import current_app

from app.cache import cache, get_key_with_prefix, set_redis_expire_seconds
from app.exceptions import UserNotFoundException
from app.models.daily_language_xp import DailyLanguageXp
from app.schemas.daily_language_xp import DailyLanguageXpSchema


class User(object):
    __slots__ = ('username', 'day_language_xp_list')

    username: str
    day_language_xp_list: List[DailyLanguageXp]

    def __init__(self, username: str) -> None:
        self.username = username

    def set_real_username(self) -> None:
        # use lowercase for cache key because it's case insensitive
        username_lower = self.username.lower()
        cache_key = get_key_with_prefix(username_lower, 'real_username')
        real_username = cache.get(cache_key)
        if real_username is None:
            response = requests.get(f'https://codestats.net/api/users/{self.username}')
            if response.status_code == requests.codes.not_found:
                raise UserNotFoundException()
            real_username = response.json()['user']
            current_app.logger.info('got real username %s for %s', real_username, self.username)
            cache.set(cache_key, real_username, timeout=24 * 60 * 60)
            current_app.logger.info('set cache [%s]', cache_key)
        # username in profile-graph api is case sensitive so set the username to the correct one
        self.username = real_username

    def get_day_language_xp_list(self, since: arrow.Arrow) -> List[DailyLanguageXp]:
        cache_key = get_key_with_prefix(f"{self.username}_{since.strftime('%Y-%m-%d')}", 'day_language_xp')
        lock_key = get_key_with_prefix(cache_key, 'lock')

        data = cache.get(cache_key)
        # add lock to make sure only one request is fetching response from server (hopefully)
        lock = cache.cache.inc(lock_key, delta=1)
        set_redis_expire_seconds(lock_key, 15)
        while data is None and isinstance(lock, int) and lock > 1:
            time.sleep(1)
            data = cache.get(cache_key)
            lock = cache.get(lock_key)

        if data is None:
            post_data = '''{
                profile(username: "%s") {
                    day_language_xps: dayLanguageXps(since: "%s") {date language xp}
                }
            }''' % (self.username, since.strftime('%Y-%m-%d'))
            response_json = requests.post('https://codestats.net/profile-graph', data=post_data).json()
            current_app.logger.info('response json from %s: %s', self.username, response_json)
            data = response_json['data']['profile']['day_language_xps']
            cache.set(cache_key, data, timeout=30 * 60)
            current_app.logger.info('set cache [%s]', cache_key)
        cache.delete(lock_key)

        self.day_language_xp_list = DailyLanguageXpSchema().load(data, many=True)
        return self.day_language_xp_list
