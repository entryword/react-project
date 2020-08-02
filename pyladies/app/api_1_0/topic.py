from flask import jsonify, request

from app.managers.topic import Manager as TopicManager
from . import api
from ..exceptions import (
    OK,
    TOPICLIST_INVALID_KEYWORD,
    TOPICLIST_INVALID_LEVEL,
    TOPICLIST_INVALID_FREQ,
    TOPICLIST_INVALID_HOST,
    TOPICLIST_INVALID_FIELDS,
    TOPICLIST_ERROR
)


@api.route("/topic/<int:t_id>", methods=["GET"])
def get_topic(t_id):
    topic_service = TopicManager()
    topic = topic_service.get_topic(t_id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=topic, info=info)

@api.route("/topics", methods=["GET"])
def list_topics():
    # event list constants
    KEYWORD_DEFAULT = ""
    KEYWORD_MAX_LEN = 30
    LEVEL_DEFAULT = None
    HOST_DEFAULT = None
    FREQ_DEFAULT = None
    FIELDS_DEFAULT = []

    keyword = request.args.get("keyword") or KEYWORD_DEFAULT
    level = request.args.get("level") or LEVEL_DEFAULT
    freq = request.args.get("freq") or FREQ_DEFAULT
    host = request.args.get("host") or HOST_DEFAULT
    fields = request.args.getlist("fields") or FIELDS_DEFAULT
    try:
        fields = set([int(i) for i in fields])
    except Exception:
        raise TOPICLIST_INVALID_FIELDS
    # validate request parameters
    if len(keyword) > KEYWORD_MAX_LEN:
        raise TOPICLIST_INVALID_KEYWORD
    if level and not level.isdigit():
        raise TOPICLIST_INVALID_LEVEL
    if freq and not freq.isdigit():
        raise TOPICLIST_INVALID_FREQ
    if host and not host.isdigit():
        raise TOPICLIST_INVALID_HOST
    # get event list from manager
    topic_manager = TopicManager()
    data = {}
    try:
        topics = topic_manager.search_topics(keyword, level, freq, host, fields)
        data = {"topics": topics, "count": len(topics)}
        info = {"code": OK.code, "message": OK.message}
    except Exception as e:
        info = {"code": TOPICLIST_ERROR.code, "message": TOPICLIST_ERROR.message}
    return jsonify(data=data, info=info)

