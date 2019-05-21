from flask import jsonify, request

from . import api
from ..exceptions import OK
from ..managers.slide import Manager as SlideManager


@api.route("/slides", methods=["GET"])
def get_slides():
    data = SlideManager.list_slides()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/slide", methods=["POST"])
def create_slide():
    request_data = request.get_json()
    data = request_data["data"]
    slide_data = {
        "type": data["type"],
        "title": data["title"],
        "url": data["url"],
    }

    manager = SlideManager()
    slide_sn = manager.create_slide(slide_data)
    slide = manager.get_slide(slide_sn)
    slide_info = {
        "id": slide.sn,
        "type": slide.type,
        "title": slide.title,
        "url": slide.url
    }
    info = {
        "code": OK.code,
        "message": OK.message,
    }

    return jsonify(data=slide_info, info=info)