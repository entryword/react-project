from flask import jsonify, request

from . import api
from ..managers.speaker import Manager as SpeakerManager
from ..exceptions import (
    OK,
    SPEAKERLIST_INVALID_KEYWORD,
    SPEAKERLIST_INVALID_FIELDS,
    SPEAKERLIST_ERROR
)

@api.route("/speaker/<int:speaker_id>", methods=["GET"])
def get_speaker_profile(speaker_id):
    speaker_service = SpeakerManager()
    speaker = speaker_service.get_speaker_profile(speaker_id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=speaker, info=info)

@api.route("/speakers", methods=["GET"])
def get_speakers():
    # retrieve query parameter
    KEYWORD_DEFAULT = ""
    KEYWORD_MAX_LEN = 30
    FIELDS_DEFAULT = []

    keyword = request.args.get("keyword") or KEYWORD_DEFAULT
    fields = request.args.getlist("fields") or FIELDS_DEFAULT

    # validate query parameter
    if len(keyword) > KEYWORD_MAX_LEN:
        raise SPEAKERLIST_INVALID_KEYWORD
    try:
        fields = {int(i) for i in fields}
    except ValueError:
        raise SPEAKERLIST_INVALID_FIELDS

    # retrieve data
    speaker_service = SpeakerManager()
    try:
        speakers = speaker_service.search_speakers(keyword, fields)
    except Exception:
        data = None
        info = {"code": SPEAKERLIST_ERROR.code, "message": SPEAKERLIST_ERROR.message}
        return jsonify(data=data, info=info)

    data = {"speakers": speakers, "count": len(speakers)}
    info = {"code": OK.code, "message": OK.message}

    return jsonify(data=data, info=info)
