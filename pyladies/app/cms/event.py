from flask import jsonify, request
from flask_login import login_required

from . import api
from ..exceptions import OK
from ..managers.event import Manager as EventManager


@api.route("/events", methods=["GET"])
@login_required
def get_events():
    data = EventManager.get_events()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/event", methods=["POST"])
@login_required
def create_event():
    request_data = request.get_json()

    data = request_data["data"]
    eventinfo = {
        "event_basic": {
            "topic_sn": data["topic_id"],
            "date": data["start_date"],
            # TODO:waiting table schema and data["end_date"] will add here
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
    event_basic_newid = em.create_event(eventinfo)
    res = {
        "data": {"id": event_basic_newid},
        "info": {"code": 0, "message": "Perform the action successfully."},
    }

    return jsonify(res)


@api.route("/event/<int:e_id>", methods=["GET"])
@login_required
def get_event(e_id):
    event_service = EventManager()
    event_info = event_service.get_event(e_id, apimode=True)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=event_info, info=info)


@api.route("/event/<int:e_id>", methods=["PUT"])
@login_required
def update_event(e_id):
    request_data = request.get_json()
    data = request_data["data"]
    eventinfo = { "event_basic": {}, "event_info": {}, "apply_info": {}}

    eventinfo = {
        "event_basic": {
            "topic_sn": data["topic_id"],
            "date": data["start_date"],
            "start_time": data["start_time"],
            "end_time": data["end_time"],
            "place_sn": data["place_id"]
        },
        "event_info": {
            "title": data["title"],
            "desc": data["desc"],
            "fields": data["field_ids"],
            "slide_resource_sns": data["slide_resource_ids"],
            "speaker_sns": data["speaker_ids"],
            "assistant_sns": data["assistant_ids"]
        },
        "apply_info": {
            "apply": data["apply"]
        }
    }

    event_service = EventManager()
    event_service.update_event(e_id, eventinfo)

    data ={
        "id":e_id
    }

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)
