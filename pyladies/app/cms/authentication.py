from flask import jsonify, request, session
from jsonschema import validate

from app.constant import UserType
from app.schemas.authentication import schema_login
from app.utils import login_required
from . import api
from ..exceptions import OK
from ..managers.user import Manager as UserManager


@api.route('/login', methods=["POST"])
def login():
    request_data = request.get_json()
    validate(request_data, schema_login)

    session['user_type'] = UserType.ADMIN
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
