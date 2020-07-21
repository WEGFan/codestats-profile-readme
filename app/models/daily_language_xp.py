# -*- coding: utf-8 -*-
import datetime


class DailyLanguageXp(object):
    __slots__ = ('language', 'date', 'xp')

    language: str
    date: datetime.date
    xp: int

    def __init__(self, language: str, date: datetime.date, xp: int) -> None:
        self.language = language
        self.date = date
        self.xp = xp

    def __repr__(self) -> str:
        class_name = type(self).__name__
        attributes = ', '.join(f'{name}={repr(getattr(self, name))}' for name in self.__slots__)
        return f'<{class_name}({attributes})>'
