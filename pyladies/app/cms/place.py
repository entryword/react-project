from flask import current_app, jsonify
from flask_login import login_required

from . import api
from ..exceptions import OK
#from ..sqldb import DBWrapper
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