from flask import jsonify, request

from app.utils import login_required
from . import api
from ..exceptions import OK
from ..managers.slide import Manager as SlideManager


@api.route("/slides", methods=["GET"])
@login_required
def get_slides():
    data = SlideManager.list_slides()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/slide", methods=["POST"])
@login_required
def create_slide():
    request_data = request.get_json()
    data = request_data["data"]
    slide_data = {
        "type": data["type"],
        "title": data["title"],
        "url": data["url"],
    }

    manager = SlideManager()
    slide_id = manager.create_slide(slide_data)
    slide = manager.get_slide(slide_id)
    slide_info = {
        "id": slide.id,
        "type": slide.type,
        "title": slide.title,
        "url": slide.url
    }
    info = {
        "code": OK.code,
        "message": OK.message,
    }

    return jsonify(data=slide_info, info=info)
