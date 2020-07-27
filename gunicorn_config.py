# -*- coding: utf-8 -*-
import os
from pathlib import Path

try:
    import config.custom_config_local as custom_config
except ImportError as err:
    import config.custom_config as custom_config

os.makedirs(custom_config.LOG_PATH, exist_ok=True)

workers = custom_config.WORKERS
worker_class = 'gevent'
bind = '127.0.0.1:2012'
daemon = True
accesslog = str(Path(custom_config.LOG_PATH, 'gunicorn_access.log').resolve())
errorlog = str(Path(custom_config.LOG_PATH, 'gunicorn.log').resolve())
loglevel = 'info'
reload = True
timeout = 60
access_log_format = '%(t)s %(l)s %({X-Real-IP}i)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
