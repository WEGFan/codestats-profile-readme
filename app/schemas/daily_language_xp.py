# -*- coding: utf-8 -*-
from marshmallow import fields, post_load, Schema

from app.models.daily_language_xp import DailyLanguageXp


class DailyLanguageXpSchema(Schema):
    language = fields.String()
    date = fields.Date()
    xp = fields.Integer()

    @post_load
    def make_object(self, data, **kwargs) -> DailyLanguageXp:
        return DailyLanguageXp(**data)
