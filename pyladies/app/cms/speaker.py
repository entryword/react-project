from flask import jsonify, request

from app.schemas.speaker_info import schema_create
from app.utils import login_required, payload_validator
from . import api
from ..constant import DEFAULT_FIELD_SN
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
@payload_validator(schema_create)
def create_speaker(payload):
    data = payload["data"]
    speaker_info = {
        "name": data["name"],
        "title": data["title"],
        "photo": data.get("photo", None),
        "major_related": data.get("major_related", True),
        "intro": data.get("intro", ""),
        "fields": data.get("fields", [DEFAULT_FIELD_SN]),
        "links": data.get("links", [])
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
@payload_validator(schema_create)
def update_speaker(speaker_id, payload):
    data = payload["data"]
    speaker_info = {
        "name": data["name"],
        "title": data["title"],
        "photo": data.get("photo", None),
        "major_related": data.get("major_related", True),
        "intro": data.get("intro", ""),
        "fields": data.get("fields", [-1]),
        "links": data.get("links", [])
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
