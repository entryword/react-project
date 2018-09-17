from flask import current_app, jsonify

from . import api
from ..exceptions import OK
from ..sqldb import DBWrapper
from ..utils import HashableDict


@api.route("/topic/<int:t_id>", methods=["GET"])
def get_topic(t_id):
    with DBWrapper(current_app.db.engine.url).session() as db_sess:
        manager = current_app.db_api_class(db_sess)
        topic = manager.get_topic(t_id)

        events = []
        speakers = set()
        assistants = set()
        slides = set()
        resources = set()
        for event_basic in topic.event_basics:
            place_info = None
            if event_basic.place:
                place_info = {
                    "name": event_basic.place.name,
                    "addr": event_basic.place.addr,
                    "map": event_basic.place.map
                }
            events.append({
                "id": event_basic.sn,
                "date": event_basic.date,
                "place_info": place_info
                })
            if event_basic.event_info:
                events[-1]["title"] = event_basic.event_info.title
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
            "name": topic.name,
            "fields": topic.fields,
            "freq": topic.freq,
            "desc": topic.desc,
            "level": topic.level,
            "events": events,
            "host": topic.host,
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
