from flask import jsonify
from flask_login import login_required

from . import api
from ..exceptions import OK
from ..managers.topic import Manager as TopicManager


@api.route("/topics", methods=["GET"])
@login_required
def get_topics():
    data = TopicManager.get_topics()

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=data, info=info)
