from flask import current_app, jsonify, request
from flask_login import login_required

from . import api
from ..exceptions import OK
from ..managers.place import Manager as PlaceManager


@api.route("/places", methods=["GET"])
@login_required
def get_places():
    data = PlaceManager.get_places()
    info = {"code": OK.code, "message": OK.message}
    return jsonify(data=data, info=info)


@api.route("/place/<int:p_id>", methods=["GET"])
@login_required
def get_place(p_id):
    data = PlaceManager.get_place(p_id)
    info = {"code": OK.code, "message": OK.message}
    return jsonify(data=data, info=info)


@api.route("/place", methods=["POST"])
@login_required
def create_place():
    request_data = request.get_json()
    data = request_data["data"]
    
    place_data = {
        "name": data["name"],
        "addr": data["addr"],
        "map": data["map"]
    }

    manager = PlaceManager()
    place_sn = manager.create_place(place_data)
    data = {"id": place_sn}
    info = {"code": OK.code, "message": OK.message}

    return jsonify(data=data, info=info)


@api.route("/place/<int:p_id>", methods=["PUT"])
@login_required
def update_place(p_id):
    request_data = request.get_json()
    data = request_data["data"]

    place_data = {
        "name": data["name"],
        "addr": data["addr"],
        "map": data["map"]
    }

    manager = PlaceManager()
    manager.update_place(p_id, place_data)
    info = {"code": OK.code, "message": OK.message}

    return jsonify(info=info)
