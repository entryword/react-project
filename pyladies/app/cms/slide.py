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
