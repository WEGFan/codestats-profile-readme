# -*- coding: utf-8 -*-
import os

os.makedirs('data/logs', exist_ok=True)

workers = 4
threads = 2
bind = '127.0.0.1:2012'
daemon = True
worker_connections = 100
accesslog = './data/logs/gunicorn_app_access.log'
errorlog = './data/logs/gunicorn_app_error.log'
loglevel = 'warning'
reload = True
timeout = 60
