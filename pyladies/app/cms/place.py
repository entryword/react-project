from flask import jsonify

from app.schemas.place_info import schema_create
from app.utils import login_required, payload_validator
from . import api
from ..exceptions import OK
from ..managers.place import Manager as PlaceManager


@api.route("/places", methods=["GET"])
@login_required
def get_places():
    data = PlaceManager.get_places()
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/place/<int:p_id>", methods=["GET"])
@login_required
def get_place(p_id):
    data = PlaceManager.get_place(p_id)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/place", methods=["POST"])
@login_required
@payload_validator(schema_create)
def create_place(payload):
    place_data = {
        "name": payload["name"],
        "addr": payload["addr"],
        "map": payload["map"]
    }
    place_id = PlaceManager.create_place(place_data)
    data = {
        "id": place_id
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/place/<int:p_id>", methods=["PUT"])
@login_required
@payload_validator(schema_create)
def update_place(p_id, payload):
    place_data = {
        "name": payload["name"],
        "addr": payload["addr"],
        "map": payload["map"]
    }
    PlaceManager.update_place(p_id, place_data)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)
