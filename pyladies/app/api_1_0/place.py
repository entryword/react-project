from flask import current_app, jsonify

from . import api
from ..exceptions import OK
from ..sqldb import DBWrapper
from ..managers.place import Manager as PlaceManager


@api.route("/places", methods=["GET"])
def get_places():
    places_services = PlaceManager()
    places = places_services.get_places()

    data = {"places": places}
    info = {"code": OK.code, "message": OK.message}

    return jsonify(data=data, info=info)
