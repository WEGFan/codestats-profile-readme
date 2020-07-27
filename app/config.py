# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

try:
    import config.custom_config_local as custom_config
except ImportError as err:
    import config.custom_config as custom_config


class Config(object):
    APP_PATH: str = str(Path(__file__).parent.resolve())
    PROJECT_PATH: str = str(Path(APP_PATH).parent.resolve())

    LOG_PATH: str = str(Path(PROJECT_PATH, custom_config.LOG_PATH).resolve())
    LOG_FILENAME: str = custom_config.LOG_FILENAME
    LOG_FORMAT: str = '[%(asctime)s] %(levelname)s - [%(module)s] [%(filename)s:%(lineno)s]: %(message)s'
    LOG_LEVEL: int = logging.DEBUG if os.getenv('FLASK_DEBUG') == '1' else logging.INFO

    CACHE_REDIS_URL: str = custom_config.REDIS_URL

    if CACHE_REDIS_URL:
        CACHE_TYPE: str = 'redis'
        CACHE_KEY_PREFIX: str = 'codestats_readme:'
    else:
        # if redis url is empty just use filesystem cache
        CACHE_TYPE: str = 'filesystem'
        CACHE_DIR: str = str(Path(PROJECT_PATH, './data/cache').resolve())
        CACHE_THRESHOLD: int = 500
        CACHE_DEFAULT_TIMEOUT: int = 15

    SVG_OPTIMIZE_ENABLE: bool = custom_config.SVG_OPTIMIZE_ENABLE
    SVGO_PATH: str = custom_config.SVGO_PATH
    SVGO_CONFIG_PATH: str = str(Path(PROJECT_PATH, custom_config.SVGO_CONFIG_PATH).resolve())
