# -*- coding: utf-8 -*-
from typing import List


class GraphConfig(object):
    __slots__ = (
        'history_days', 'max_languages', 'language_colors', 'timezone', 'width', 'height',
        'bg_color', 'show_legend', 'grid_color', 'text_color', 'zeroline_color'
    )

    history_days: int
    max_languages: int
    language_colors: List[str]
    timezone: str
    width: int
    height: int
    bg_color: str
    show_legend: bool
    grid_color: str
    text_color: str
    zeroline_color: str

    def __init__(self) -> None:
        self.history_days = 14
        self.max_languages = 8
        self.language_colors = [
            '#3e4053', '#f15854', '#5da5da', '#faa43a', '#60bd68',
            '#f17cb0', '#b2912f', '#decf3f', '#b276b2'
        ]
        self.timezone = '00:00'
        self.width = 900
        self.height = 450
        self.bg_color = '#ffffff'
        self.show_legend = True
        self.grid_color = '#e8e8e8'
        self.text_color = '#666666'
        self.zeroline_color = '#ababab'

    def update(self, **kwargs) -> None:
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def __repr__(self) -> str:
        class_name = type(self).__name__
        attributes = ', '.join(f'{name}={repr(getattr(self, name))}' for name in self.__slots__)
        return f'<{class_name}({attributes})>'
