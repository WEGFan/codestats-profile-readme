# -*- coding: utf-8 -*-
from flask import Response, current_app, render_template
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.exceptions import UserNotFoundException


def user_not_found(error: UserNotFoundException):
    return Response(render_template('error.svg', message='User not found or private.'), mimetype='image/svg+xml',
                    headers={
                        'Cache-Control': 'max-age=0'
                    })


def validation_error(error: ValidationError):
    current_app.logger.warning('invalid args: %s', error.messages)
    return Response(render_template('validation_error.svg', error=error.messages),
                    mimetype='image/svg+xml',
                    headers={
                        'Cache-Control': 'max-age=0'
                    })


def http_exception(error: HTTPException):
    return error


def internal_server_error(error: Exception):
    current_app.logger.exception(error)
    return Response(render_template('error.svg', message='Internal server error.'), mimetype='image/svg+xml',
                    headers={
                        'Cache-Control': 'max-age=0'
                    })
