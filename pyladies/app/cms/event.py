from flask import current_app, jsonify, request

from . import api
from ..exceptions import (
    OK,
    EVENTLIST_INVALID_KEYWORD,
    EVENTLIST_INVALID_DATE,
    EVENTLIST_INVALID_SORT,
    EVENTLIST_INVALID_ORDER,
    EVENTLIST_ERROR,
)
from ..managers.event import Manager as EventManager
from ..sqldb import DBWrapper
from ..utils import HashableDict, validate_time_format


@api.route("/event", methods=["POST"])
def createEvent():
    request_data = request.get_json()

    data = request_data["data"]
    eventinfo = {
        "event_basic": {
            "topic_sn": data["topic_id"],
            "date": data["start_date"],
            "start_time": data["start_time"],
            "end_time": data["end_time"],
            "place_sn": data["place_id"],
        },
        "event_info": {
            "event_basic_sn": None,
            "title": data["title"],
            "desc": data["desc"],
            "fields": data["field_ids"],
            "speaker_sns": data["speaker_ids"],
            "assistant_sns": data["assistant_ids"],
        },
    }

    em = EventManager()
    try:
        event_basic_newid = em.create_event(eventinfo)
    except Exception as e:
        data = None
        info = {"code": EVENTLIST_ERROR.code, "message": EVENTLIST_ERROR.message}
        print(e)
        return jsonify(data=data, info=info)

    res = {
        "data": {"id": event_basic_newid},
        "info": {"code": 0, "message": "Perform the action successfully."},
    }

    return jsonify(res)