import importlib
from datetime import datetime
from functools import partial, wraps

from flask import request, current_app, jsonify
from flask_login import current_user
from jsonschema import validate

from .constant import UserType
from .exceptions import OK


def import_class(module_class_name):
    module_name, _, class_name = module_class_name.rpartition('.')
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def validate_time_format(time_str, expected_format, err_message=''):
    try:
        datetime.strptime(time_str, expected_format)
    except Exception:
        raise ValueError(err_message)


def payload_validator(payload_field):
    def real_decorator(method, **kwargs):

        @wraps(method)
        def wrapper(*args, **kwargs):
            payload = request.get_json(force=True)
            validate(payload, payload_field)

            return method(*args, **kwargs, payload=payload)

        return wrapper

    return real_decorator


def json_response(data=None):
    info = {
        'code': OK.code,
        'message': OK.message
    }
    if data is None:
        return jsonify(info=info)

    return jsonify(data=data, info=info)


def login_required(func=None, user_type=UserType.ADMIN):
    if func is None:
        return partial(login_required, user_type=user_type)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        if not (current_user.is_authenticated and current_user.type == user_type):
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return wrapper


def permit_params(params, keys):
    return {key: value for key, value in params.items() if key in keys}
