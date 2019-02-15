from flask import current_app, jsonify

from . import api
from ..exceptions import OK
from ..sqldb import DBWrapper

@api.route("/apply/<int:e_sn>", methods=["GET"])
def get_event_apply_info(e_sn):
    with DBWrapper(current_app.db.engine.url).session() as db_sess:
        manager = current_app.db_api_class(db_sess)
        event_apply_info = manager.get_event_apply_info(e_sn)

        data = {
            "event_apply_info": event_apply_info
        }

        info = {
            "code": OK.code,
            "message": OK.message
        }

        return jsonify(data=data, info=info)
        