from flask import jsonify

from app.schemas.role_info import schema_create
from app.utils import login_required, payload_validator
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


@api.route("/role/<int:id>", methods=["GET"])
@login_required
def get_role(id):
    data = RoleManager.get_role(id)

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
    id = RoleManager.create_role(create_info)

    return_info = {
        "code": OK.code,
        "message": OK.message
    }
    return_data = {"id": id}

    return jsonify(data=return_data, info=return_info)


@api.route("/role/<int:id>", methods=["PUT"])
@login_required
@payload_validator(schema_create)
def update_role(id, payload):
    update_info = {
        "name": payload["name"],
        "permission": payload["permission"],
    }
    RoleManager.update_role(id, update_info)

    return_info = {
        "code": OK.code,
        "message": OK.message
    }
    return_data = {"id": id}

    return jsonify(data=return_data, info=return_info)


@api.route("/role/<int:id>", methods=["DELETE"])
@login_required
def delete_role(id):
    RoleManager.delete_role(id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(info=info)
