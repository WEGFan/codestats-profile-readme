# -*- coding: utf-8 -*-
import json
from json.decoder import JSONDecodeError

from marshmallow import Schema, ValidationError, fields, post_load, validate
from marshmallow.decorators import pre_load

from app.fields import ColorString, TimezoneString
from app.models.history_graph_config import GraphConfig


class GraphConfigSchema(Schema):
    history_days = fields.Integer(validate=validate.Range(min=1, max=30))
    max_languages = fields.Integer(validate=validate.Range(min=0, max=15))
    language_colors = fields.List(ColorString())
    timezone = TimezoneString()
    bg_color = ColorString()
    width = fields.Integer(validate=validate.Range(min=10))
    height = fields.Integer(validate=validate.Range(min=10))
    show_legend = fields.Boolean()
    grid_color = ColorString()
    text_color = ColorString()
    zeroline_color = ColorString()

    @pre_load
    def parse_list(self, data, **kwargs):
        field_name_list = ['language_colors']

        for field_name in field_name_list:
            if field_name not in data:
                continue
            value = data[field_name]
            if isinstance(value, list):
                continue
            try:
                parsed_list = json.loads(data[field_name])
            except JSONDecodeError as err:
                raise ValidationError(f'Invalid list string: {value}', field_name)
            if not isinstance(parsed_list, list):
                raise ValidationError(f'Not a list: {value}', field_name)
            data[field_name] = parsed_list
        print(data)
        return data

    @post_load
    def make_object(self, data, **kwargs) -> GraphConfig:
        config = GraphConfig()
        config.update(**data)
        return config
