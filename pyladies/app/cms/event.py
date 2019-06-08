from flask import jsonify, request

from . import api
from ..exceptions import OK
from ..managers.event import Manager as EventManager


@api.route("/events", methods=["GET"])
def get_events():
    data = EventManager.get_events()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/event", methods=["POST"])
def createEvent():
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
def get_event(e_id):
    event_service = EventManager()
    event_info = event_service.get_event(e_id, apimode=True)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=event_info, info=info)
    
    
@api.route("/event/<int:e_id>", methods=["PUT"])
def put_event(e_id):
    request_data = request.get_json()
    data = request_data["data"]
    eventinfo = {"event_basic": {},"event_info": {},}

    if  data["topic_id"]: eventinfo["event_basic"]["topic_sn"] =  data["topic_id"]
    if  data["start_date"]: eventinfo["event_basic"]["date"] =  data["start_date"]
    # TODO:waiting table schema and data["end_date"] will add here
    if  data["start_time"]: eventinfo["event_basic"]["start_time"] =  data["start_time"]
    if  data["end_time"]: eventinfo["event_basic"]["end_time"] =  data["end_time"]
    if  data["place_id"]: eventinfo["event_basic"]["place_sn"] =  data["place_id"]
    if  data["title"]: eventinfo["event_info"]["title"] =  data["title"]
    if  data["desc"]: eventinfo["event_info"]["desc"] =  data["desc"]
    if  data["field_ids"]: eventinfo["event_info"]["fields"] =  data["field_ids"]
    if  data["slide_resource_ids"]: eventinfo["event_info"]["slide_resource_sns"] =  data["slide_resource_ids"]
    if  data["speaker_ids"]: eventinfo["event_info"]["speaker_sns"] =  data["speaker_ids"]
    if  data["assistant_ids"]: eventinfo["event_info"]["assistant_sns"] =  data["assistant_ids"]

    event_service = EventManager()
    event_info = event_service.update_event(e_id, eventinfo)

    data ={
        "id":e_id
    }

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)

