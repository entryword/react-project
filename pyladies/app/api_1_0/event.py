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
    with DBWrapper(current_app.db.engine.url).session() as db_sess:
        manager = current_app.db_api_class(db_sess)
        event_basic = manager.get_event_basic(e_id)

        place_info = None
        if event_basic.place:
            place_info = {
                "name": event_basic.place.name,
                "addr": event_basic.place.addr,
                "map": event_basic.place.map
            }

        title = None
        fields = []
        desc = None
        speakers = set()
        assistants = set()
        slides = set()
        resources = set()
        if event_basic.event_info:
            title = event_basic.event_info.title
            fields = event_basic.event_info.fields
            desc = event_basic.event_info.desc
            if event_basic.event_info.speakers:
                for speaker in event_basic.event_info.speakers:
                    speaker_info = HashableDict({
                        "id": speaker.sn,
                        "name": speaker.name,
                        "photo": speaker.photo
                    })
                    speakers.add(speaker_info)
            if event_basic.event_info.assistants:
                for assistant in event_basic.event_info.assistants:
                    assistant_info = HashableDict({
                        "id": assistant.sn,
                        "name": assistant.name,
                        "photo": assistant.photo
                    })
                    assistants.add(assistant_info)
            if event_basic.event_info.slide_resources:
                for data in event_basic.event_info.slide_resources:
                    if data.type == "slide":
                        slide_info = HashableDict({
                            "id": data.sn,
                            "title": data.title,
                            "url": data.url
                            })
                        slides.add(slide_info)
                    else:
                        resource_info = HashableDict({
                            "id": data.sn,
                            "title": data.title,
                            "url": data.url
                            })
                        resources.add(resource_info)

        slides = sorted(slides, key=lambda x: x["id"])
        for slide in slides:
            del slide["id"]
        resources = sorted(resources, key=lambda x: x["id"])
        for resource in resources:
            del resource["id"]

        data = {
            "topic_info": {
                "name": event_basic.topic.name,
                "id": event_basic.topic.sn
            },
            "title": title,
            "fields": fields,
            "desc": desc,
            "level": event_basic.topic.level,
            "date": event_basic.date,
            "start_time": event_basic.start_time,
            "end_time": event_basic.end_time,
            "place_info": place_info,
            "host": event_basic.topic.host,
            "speakers": list(speakers),
            "assistants": list(assistants),
            "slides": list(slides),
            "resources": list(resources)
        }
        info = {
            "code": OK.code,
            "message": OK.message
        }

        return jsonify(data=data, info=info)

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
        "count": len(events),
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)
