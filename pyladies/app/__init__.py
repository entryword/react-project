from flask import Flask, jsonify, current_app

from config import config

from app.exceptions import PyLadiesException, ROUTING_NOT_FOUND, UNEXPECTED_ERROR
from app.sqldb.models import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    app.db = db

    # blueprint registration
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/v1.0/api')

    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(PyLadiesException, handle_pyladies_error)
    app.register_error_handler(Exception, handle_unexpected_error)

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


def handle_unexpected_error(error):
    # TODO: logging
    import traceback
    print(traceback.format_exc())
    info = {
        "code": UNEXPECTED_ERROR.code,
        "message": UNEXPECTED_ERROR.message
    }
    return jsonify(info=info), 500
