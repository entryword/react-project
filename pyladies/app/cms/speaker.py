from flask import current_app, jsonify, request
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


@api.route("/speaker", methods=["POST"])
@login_required
def create_speaker():
    request_data = request.get_json()

    data = request_data["data"]
    speaker_info = {
        "name": data["name"],
        "photo": data["photo"],
        "title": data["title"],
        "major_related": data["major_related"],
        "intro": data["intro"],
        "fields": data["fields"],
        "links": data["links"]
    }

    speaker_new_id = SpeakerManager().create_speaker_by_object(speaker_info)
    res = {
        "data": {"id": speaker_new_id},
        "info": {"code": 0, "message": "Perform the action successfully."},
    }

    return jsonify(res)


@api.route("/speaker/<int:speaker_id>", methods=["GET"])
@login_required
def get_speaker(speaker_id):
    speaker_info = SpeakerManager.get_speaker(speaker_id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=speaker_info, info=info)


@api.route("/speaker/<int:speaker_id>", methods=["PUT"])
@login_required
def update_speaker(speaker_id):
    request_data = request.get_json()
    data = request_data["data"]

    speaker_info = {
        "name": data["name"],
        "photo": data["photo"],
        "title": data["title"],
        "major_related": data["major_related"],
        "intro": data["intro"],
        "fields": data["fields"],
        "links": data["links"]
    }

    SpeakerManager().update_speaker_by_object(speaker_id, speaker_info)

    data = {
        "id": speaker_id
    }

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)


@api.route("/speaker/<int:speaker_id>", methods=["DELETE"])
@login_required
def delete_speaker(speaker_id):
    SpeakerManager.delete_speaker(speaker_id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(info=info)
