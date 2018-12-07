from flask import jsonify, abort

from app.constant import DEFINITION_1_0
from app.exceptions import OK
from . import api


@api.route("/definitions", methods=["GET"])
def get_definitions():
    data = {}
    for key, value in DEFINITION_1_0.items():
        data[key] = {k: v for k, v in value.items()}

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/definition/<key>", methods=["GET"])
def get_definition(key):
    if key not in DEFINITION_1_0:
        abort(404)

    data = DEFINITION_1_0[key]
    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)
