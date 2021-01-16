import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, jsonify, current_app, redirect, url_for, session
from flask_login import LoginManager
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import Unauthorized

from config import config

from app.exceptions import (
    PyLadiesException, ROUTING_NOT_FOUND, UNEXPECTED_ERROR,
    USER_LOGIN_REQUIRED, INVALID_INPUT,
)
from app.sqldb.models import db, AnonymousUser, User


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    app.db = db

    login_manager.init_app(app)

    # blueprint registration
    from .api_1_0 import api as api_1_0_blueprint
    from .cms import api as cms_api_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/v1.0/api')
    app.register_blueprint(cms_api_blueprint, url_prefix='/cms/api')

    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(PyLadiesException, handle_pyladies_error)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(Unauthorized, handle_unauthorized_error)
    app.register_error_handler(Exception, handle_unexpected_error)

    # Session config
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

    # OAuth Setup
    os.environ['GOOGLE_CLIENT_ID'] = '18018907994-vnhv9gqqlp4fkhek12pejafa5sp9bmcr.apps.googleusercontent.com'
    os.environ['GOOGLE_CLIENT_SECRET'] = 'O4GaZWAaXffzdyytNPWpcxx4'

    oauth = OAuth(app)
    oauth.register(
        name='google',
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'},
    )
    app.oauth = oauth

    return app

def handle_not_found_error(error):
    # TODO: logging
    info = {
        "code": ROUTING_NOT_FOUND.code,
        "message": ROUTING_NOT_FOUND.message
    }
    return jsonify(info=info), 404


def handle_pyladies_error(error):
    # TODO: logging
    info = {
        "code": error.code,
        "message": error.message
    }
    return jsonify(info=info)


def handle_validation_error(error):
    # TODO: logging
    import traceback
    print(traceback.format_exc())
    info = {
        "code": INVALID_INPUT.code,
        "message": INVALID_INPUT.message
    }
    return jsonify(info=info)


def handle_unauthorized_error(error):
    info = {
        "code": USER_LOGIN_REQUIRED.code,
        "message": USER_LOGIN_REQUIRED.message
    }
    return jsonify(info=info)


def handle_unexpected_error(error):
    # TODO: logging
    import traceback
    print(traceback.format_exc())
    info = {
        "code": UNEXPECTED_ERROR.code,
        "message": UNEXPECTED_ERROR.message
    }
    return jsonify(info=info), 500
