# -*- coding: utf-8 -*-
import re

import arrow
from _plotly_utils.basevalidators import ColorValidator
from dateutil.tz import tzoffset
from marshmallow import fields, ValidationError


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
            parsed = arrow.parser.TzinfoParser.parse(value)
            if isinstance(parsed, tzoffset):
                offset = parsed.utcoffset(None).total_seconds()
                if not -12 <= offset / 60 / 60 <= 12:
                    raise ValidationError(f'Invalid timezone string: {value}, must between -12:00 and +12:00')
            return value
        except arrow.ParserError as err:
            raise ValidationError(f'Invalid timezone string: {value}') from err
