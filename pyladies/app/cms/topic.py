from flask import jsonify, request
from flask_login import login_required

from . import api
from ..exceptions import OK, TOPIC_NOT_EXIST, PyLadiesException
from ..managers.topic import Manager as TopicManager
from ..logger.core import logger

@api.route("/topics", methods=["GET"])
@login_required
def get_topics():
    data = TopicManager.get_topics()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)

@api.route("/topic/<int:t_id>", methods=["GET"])
@login_required
def get_topic(t_id):
    data = TopicManager.get_topic(t_id)
    data = {
                "name": data["name"],
                "desc": data["desc"],
                "freq": data["freq"],
                "level": data["level"],
                "host": data["host"],
                "fields": data["fields"]
            }
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)

@api.route("/topic", methods=["POST"])
@login_required
def create_topic():
    request_data = request.get_json()

    data = request_data["data"]
    topic_info = {
        "name": data["name"],
        "desc": data["desc"],
        "freq": data["freq"],
        "level": data["level"],
        "host": data["host"],
        "fields": data["fields"],
    }

    topic_sn = TopicManager().create_topic_by_object(topic_info)
    data = {
        "id": topic_sn
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)

@api.route("/topic/<int:t_id>", methods=["PUT"])
@login_required
def update_topic(t_id):
    request_data = request.get_json()
    data = request_data["data"]
    topic_info = {
        "name": data["name"],
        "desc": data["desc"],
        "freq": data["freq"],
        "level": data["level"],
        "host": data["host"],
        "fields": data["fields"],
    }
    TopicManager.update_topic_by_object(t_id, topic_info)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)
    
@api.route("/topic/<int:t_id>", methods=["DELETE"])
@login_required
def delete_topic(t_id):
    try:
        data = TopicManager.get_topic(t_id)
        TopicManager.delete_topic(t_id)
        logger.debug("Delete topic '{}'".format(data["name"]))
    except PyLadiesException as e:
        if e.code == TOPIC_NOT_EXIST.code:
            logger.debug("Delete topic failed: topic does not exist.")
            pass
        else:
            logger.debug("Delete topic failed: unexpected error.")
            raise

    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)
