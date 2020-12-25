from flask import Flask, jsonify, current_app, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
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
    app.secret_key = os.getenv("APP_SECRET_KEY")
    app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

    # oAuth Setup
    oauth = OAuth(app)
    google = oauth.register(
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

    return app


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


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
