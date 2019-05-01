from flask import jsonify, request
from flask_login import login_required
from jsonschema import validate

from . import api
from ..exceptions import OK
from ..managers.user import Manager as UserManager
from app.schemas.authentication import schema_login


@api.route('/login', methods=["POST"])
def login():
    request_data = request.get_json()
    validate(request_data, schema_login)

    UserManager.login(request_data["username"], request_data["password"])
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)


@api.route('/logout', methods=["PUT"])
@login_required
def logout():
    UserManager.logout()
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)
