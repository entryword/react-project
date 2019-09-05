from flask import current_app, jsonify
from flask_login import login_required

from . import api
from ..exceptions import OK
from ..managers.speaker import Manager as SpeakerManager


@api.route("/speakers", methods=["GET"])
@login_required
def get_speakers():
    data = SpeakerManager.get_speakers()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)
