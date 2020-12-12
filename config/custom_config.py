# -*- coding: utf-8 -*-

# NOTE:
# You can duplicate this file as custom_config_local.py in this folder, the application will try to load config in
# custom_config_local.py before custom_config.py.
#
# All paths below are relative to the project folder (which is where run.py at)
# Absolute paths also supported. e.g. /var/log/

# WORKERS: The number of worker processes for handling requests.
WORKERS: int = 4

# LOG_PATH: Where log file stores in. Default is ./data/logs
LOG_PATH: str = r'./data/logs'

# LOG_FILENAME: The log file's filename.
LOG_FILENAME: str = 'app.log'

# REDIS_URL: The URL to connect to a Redis server. e.g. redis://user:password@localhost:6379/0
# If empty, a filesystem cache will be used under ./data/cache
REDIS_URL: str = ''

# SVG_OPTIMIZE_ENABLE: Whether or not to optimize SVGs with SVGO before response.
# npm and SVGO is needed to be installed.
SVG_OPTIMIZE_ENABLE: bool = False

# SVGO_PATH: Specifies the path to SVGO.
SVGO_PATH: str = r'/usr/bin/svgo'

# SVGO_CONFIG_PATH: Specifies the path to the config file of SVGO.
SVGO_CONFIG_PATH: str = r'./config/svgo.yml'

USERNAME: str = 'grigala'
IGNORE_LIST: list = ['Plain text',
                     'nerdtree',
                     'Markdown',
                     'Properties',
                     'XML',
                     'JSON',
                     'vim-plug',
                     'scminput']
