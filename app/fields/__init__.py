# -*- coding: utf-8 -*-
import re

import arrow
from _plotly_utils.basevalidators import ColorValidator
from marshmallow import ValidationError, fields


class ColorString(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        super()._deserialize(value, attr, data, **kwargs)
        try:
            # 'aaa' -> '#aaa', 'aabbcc' -> '#aabbcc'
            if re.fullmatch(r'[0-9A-Fa-f]*', value) and len(value) in (3, 6):
                value = '#' + value
            return ColorValidator('', '').validate_coerce(value)
        except ValueError as err:
            raise ValidationError(f'Invalid color string: {value}') from err


class TimezoneString(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        super()._deserialize(value, attr, data, **kwargs)
        try:
            value = value.strip()
            arrow.parser.TzinfoParser.parse(value)
            return value
        except arrow.ParserError as err:
            raise ValidationError(f'Invalid timezone string: {value}') from err
