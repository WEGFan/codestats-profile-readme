# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path


class Config(object):
    APP_PATH: str = str(Path(__file__).parent.resolve())
    PROJECT_PATH: str = str(Path(APP_PATH).parent.resolve())

    LOG_PATH: str = str(Path(PROJECT_PATH, 'data', 'logs').resolve())
    LOG_FILENAME: str = 'app.log'
    LOG_FORMAT: str = '[%(asctime)s] %(levelname)s - [%(module)s] [%(filename)s:%(lineno)s]: %(message)s'
    LOG_LEVEL: int = logging.DEBUG if os.getenv('FLASK_DEBUG') == '1' else logging.INFO

    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_KEY_PREFIX = 'codestats_readme:'
    CACHE_DIR = str(Path(PROJECT_PATH, 'data', 'cache').resolve())
    CACHE_THRESHOLD = 500
    CACHE_DEFAULT_TIMEOUT = 15

    SVGO_PATH = 'svgo'
    SVGO_CONFIG_PATH = str(Path(APP_PATH, 'svgo.yml').resolve())
