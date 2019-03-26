from flask import current_app, jsonify, request

from . import api
from ..exceptions import (
    OK, EVENTLIST_INVALID_KEYWORD, EVENTLIST_INVALID_DATE,
    EVENTLIST_INVALID_SORT, EVENTLIST_INVALID_ORDER, EVENTLIST_ERROR)
from ..managers.event import Manager as EventManager
from ..sqldb import DBWrapper
from ..utils import HashableDict, validate_time_format


@api.route("/event/<int:e_id>", methods=["GET"])
def get_event(e_id):
    event_service = EventManager()
    event_info = event_service.get_event(e_id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=event_info, info=info)

@api.route("/event", methods=["POST"])
def createEvent():
    request_data = request.get_json()

    data = request_data["data"]
    event_basic = {
        "topic_sn": data["topic_id"],
        "date": data["start_date"],
        "start_time": data["start_time"],
        "end_time": data["end_time"],
        "place_sn": data["place_id"],
    }

    
    with DBWrapper(self.app.db.engine.url).session() as db_sess:
        manager = self.app.db_api_class(db_sess)
        event_basic_newid = manager.create_event_basic(event_basic, autocommit=True)

    event_info_info = {
        "event_basic_sn": event_basic_newid,
        "title": data["title"],
        "desc": data["desc"],
        "fields": data["field_ids"],
        "speaker_sns":data["speaker_ids"],
        "assistant_sns":data["assistant_ids"],

    }
    with DBWrapper(self.app.db.engine.url).session() as db_sess:
        manager = self.app.db_api_class(db_sess)
        manager.create_event_info(event_info_info, autocommit=True)

    res ={"data":{"id":event_basic_newid},"info":{"code":0,"message":"Perform the action successfully."}}

    return jsonify(res)



@api.route("/events", methods=["GET"])
def list_events():
    # event list constants
    EVENTLIST_PARAM_KEYWORD_DEFAULT = ""
    EVENTLIST_PARAM_KEYWORD_MAX_LEN = 30
    EVENTLIST_PARAM_DATE_DEFAULT = ""
    EVENTLIST_PARAM_SORT_DEFAULT = "date"
    EVENTLIST_PARAM_SORT_OPTIONS = ["date"]
    EVENTLIST_PARAM_ORDER_DEFAULT = "asc"
    EVENTLIST_PARAM_ORDER_OPTIONS = ["asc", "desc"]

    keyword = request.args.get("keyword", EVENTLIST_PARAM_KEYWORD_DEFAULT) \
    or EVENTLIST_PARAM_KEYWORD_DEFAULT
    date = request.args.get("date", EVENTLIST_PARAM_DATE_DEFAULT) \
    or EVENTLIST_PARAM_DATE_DEFAULT
    sort = request.args.get("sort", EVENTLIST_PARAM_SORT_DEFAULT) \
    or EVENTLIST_PARAM_SORT_DEFAULT
    order = request.args.get("order", EVENTLIST_PARAM_ORDER_DEFAULT) \
    or EVENTLIST_PARAM_ORDER_DEFAULT

    # validate request parameters
    if len(keyword) > EVENTLIST_PARAM_KEYWORD_MAX_LEN:
        raise EVENTLIST_INVALID_KEYWORD

    if date:
        try:
            validate_time_format(date, '%Y-%m')
        except ValueError:
            raise EVENTLIST_INVALID_DATE

    if not sort in EVENTLIST_PARAM_SORT_OPTIONS:
        raise EVENTLIST_INVALID_SORT

    if not order in EVENTLIST_PARAM_ORDER_OPTIONS:
        raise EVENTLIST_INVALID_ORDER

    # get event list from manager
    em = EventManager()
    try:
        events = em.search_events(keyword, date, sort, order)
    except Exception:
        data = None
        info = {
            "code": EVENTLIST_ERROR.code,
            "message": EVENTLIST_ERROR.message,
        }
        return jsonify(data=data, info=info)

    data = {
        "events": events,
        "count": len(events)
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/events_from_distinct_topics", methods=["GET"])
def get_events_from_distinct_topics():
    em = EventManager()
    events = em.get_events_from_distinct_topics(4)

    data = {
        "events": events
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)
