from flask import current_app, jsonify

from . import api
from ..exceptions import OK
from ..sqldb import DBWrapper
#from ..utils import HashableDict


@api.route("/places/", methods=["GET"])
def get_places():
    with DBWrapper(current_app.db.engine.url).session() as db_sess:
        manager = current_app.db_api_class(db_sess)
        places = manager.get_places()

        places_list = []
        for place in places:
            data = {
                "name": place.name,
                "addr": place.addr,
                "map": place.map
            }
            places_list.append(data)
        data = {
            "places": places_list
        }
        info = {
            "code": OK.code,
            "message": OK.message
        }

        return jsonify(data=data, info=info)
