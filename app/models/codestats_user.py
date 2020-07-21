# -*- coding: utf-8 -*-
import arrow
import requests
from flask import current_app

from app.schemas.daily_language_xp import DailyLanguageXpSchema


class User(object):
    __slots__ = ('username', 'day_language_xp_list')

    def __init__(self, username: str) -> None:
        self.username = username

    def exists(self):
        response = requests.get(f'https://codestats.net/api/users/{self.username}')
        if response.status_code == requests.codes.not_found:
            return False
        return True

    def get_day_language_xp_list(self, since: arrow.Arrow):
        post_data = '''{
            profile(username: "%s") {
                day_language_xps: dayLanguageXps(since: "%s") {date language xp}
            }
        }''' % (self.username, since.strftime('%Y-%m-%d'))
        response_json = requests.post('https://codestats.net/profile-graph', data=post_data).json()
        current_app.logger.info('response json from %s: %s', self.username, response_json)
        data = response_json['data']['profile']['day_language_xps']
        return DailyLanguageXpSchema().load(data, many=True)
