from flask import current_app, jsonify

from . import api
from ..exceptions import OK
from ..sqldb import DBWrapper


@api.route("/apply/<int:event_basic_id>", methods=["GET"])
def get_event_apply_info(event_basic_id):
    with DBWrapper(current_app.db.engine.url).session() as db_sess:
        manager = current_app.db_api_class(db_sess)
        event_apply_info = manager.get_event_apply_info(event_basic_id)

        data = {
            "event_basic_id":event_apply_info.event_basic_id,
            "host": event_apply_info.host,
            "start_time": event_apply_info.start_time,
            "end_time": event_apply_info.end_time,
            "apply":event_apply_info.apply,
            "limit":event_apply_info.limit,
            "limit_desc": event_apply_info.limit_desc
        }
        info = {
            "code": OK.code,
            "message": OK.message
        }

        return jsonify(data=data, info=info)
        