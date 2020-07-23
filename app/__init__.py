# -*- coding: utf-8 -*-
import logging
import logging.handlers
from pathlib import Path

from flask import Flask
from werkzeug.exceptions import HTTPException

from app import controllers
from . import config

from app.controllers.home import home
from app.controllers.history_graph import history_graph

from app.exceptions import UserNotFoundException
from app.error_handlers import internal_server_error, validation_error, user_not_found, http_exception
from marshmallow.exceptions import ValidationError


def create_app(config_object=config.Config):
    app = Flask(__name__, root_path=config_object.APP_PATH)
    with app.app_context():
        app.config.from_object(config_object)

        log_file_path = Path(app.config['LOG_PATH'])
        log_file_path.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(Path(log_file_path, app.config['LOG_FILENAME']), encoding='utf-8')
        handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
        app.logger.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(handler)

        app.jinja_env.auto_reload = True

        app.register_blueprint(home)
        app.register_blueprint(history_graph)

        app.register_error_handler(UserNotFoundException, user_not_found)
        app.register_error_handler(ValidationError, validation_error)
        app.register_error_handler(HTTPException, http_exception)
        app.register_error_handler(Exception, internal_server_error)

        return app
