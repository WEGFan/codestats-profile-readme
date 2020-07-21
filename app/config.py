# -*- coding: utf-8 -*-
import logging
from pathlib import Path


class Config(object):
    APP_PATH: str = str(Path(__file__).parent.resolve())
    PROJECT_PATH: str = str(Path(APP_PATH).parent.resolve())

    LOG_PATH: str = str((Path(PROJECT_PATH) / 'data' / 'logs').resolve())
    LOG_FILENAME: str = 'app.log'
    LOG_FORMAT: str = '[%(asctime)s] %(levelname)s - [%(module)s] [%(filename)s:%(lineno)s]: %(message)s'
    LOG_LEVEL: int = logging.INFO
