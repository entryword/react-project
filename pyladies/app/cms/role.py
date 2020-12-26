from flask import jsonify
from flask_login import login_required

from app.schemas.role_info import schema_create
from app.utils import payload_validator
from . import api
from ..exceptions import OK
from ..managers.role import Manager as RoleManager


@api.route("/roles", methods=["GET"])
@login_required
def get_roles():
    data = RoleManager.get_roles()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/role/<int:sn>", methods=["GET"])
@login_required
def get_role(sn):
    data = RoleManager.get_role(sn)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/role", methods=["POST"])
@login_required
@payload_validator(schema_create)
def create_role(payload):
    create_info = {
        "name": payload["name"],
        "permission": payload["permission"],
    }
    sn = RoleManager.create_role(create_info)

    return_info = {
        "code": OK.code,
        "message": OK.message
    }
    return_data = {"id": sn}

    return jsonify(data=return_data, info=return_info)


@api.route("/role/<int:sn>", methods=["PUT"])
@login_required
@payload_validator(schema_create)
def update_role(sn, payload):
    update_info = {
        "name": payload["name"],
        "permission": payload["permission"],
    }
    RoleManager.update_role(sn, update_info)

    return_info = {
        "code": OK.code,
        "message": OK.message
    }
    return_data = {"id": sn}

    return jsonify(data=return_data, info=return_info)


@api.route("/role/<int:sn>", methods=["DELETE"])
@login_required
def delete_role(sn):
    RoleManager.delete_role(sn)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(info=info)
