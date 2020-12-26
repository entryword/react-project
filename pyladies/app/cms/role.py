from flask import jsonify, request
from flask_login import login_required

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
def create_role():
    request_data = request.get_json()
    data = request_data["data"]

    create_info = {
        "name": data["name"],
        "permission": data["permission"],
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
def update_role(sn):
    request_data = request.get_json()
    data = request_data["data"]

    update_info = {
        "name": data["name"],
        "permission": data["permission"],
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
