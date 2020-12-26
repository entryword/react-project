from flask import jsonify
from flask_login import login_required

from app.schemas.event_basic_info import schema_create
from app.utils import payload_validator
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
@payload_validator(schema_create)
def create_event(payload):
    event_info = {
        "event_basic": {
            "topic_sn": payload["topic_id"],
            "date": payload["start_date"],
            # TODO:waiting table schema and payload["end_date"] will add here
            "start_time": payload["start_time"],
            "end_time": payload["end_time"],
            "place_sn": payload["place_id"],
        },
        "event_info": {
            "title": payload["title"],
            "desc": payload["desc"],
            "fields": payload["field_ids"],
            "speaker_sns": payload["speaker_ids"],
            "assistant_sns": payload["assistant_ids"],
        },
    }
    new_id = EventManager.create_event(event_info)
    data = {
        "id": new_id
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/event/<int:e_id>", methods=["GET"])
@login_required
def get_event(e_id):
    data = EventManager.get_event(e_id, apimode=True)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/event/<int:e_id>", methods=["PUT"])
@login_required
@payload_validator(schema_create)
def update_event(e_id, payload):
    event_info = {
        "event_basic": {
            "topic_sn": payload["topic_id"],
            "date": payload["start_date"],
            "start_time": payload["start_time"],
            "end_time": payload["end_time"],
            "place_sn": payload["place_id"]
        },
        "event_info": {
            "title": payload["title"],
            "desc": payload["desc"],
            "fields": payload["field_ids"],
            "slide_resource_sns": payload["slide_resource_ids"],
            "speaker_sns": payload["speaker_ids"],
            "assistant_sns": payload["assistant_ids"]
        },
        "apply_info": {
            "apply": payload["apply"]
        }
    }

    EventManager.update_event(e_id, event_info)

    data = {
        "id": e_id
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/event/<int:e_id>", methods=["DELETE"])
@login_required
def delete_event(e_id):
    EventManager.delete_event(e_id)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)
