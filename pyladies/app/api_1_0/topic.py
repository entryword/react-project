from flask import jsonify
from app.managers.topic import Manager as TopicManager
from . import api
from ..exceptions import OK


@api.route("/topic/<int:t_id>", methods=["GET"])
def get_topic(t_id):
    topic_service = TopicManager()
    topic = topic_service.get_topic(t_id)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=topic, info=info)
