from flask import jsonify

from app.managers import apply
from . import api
from ..exceptions import OK


@api.route("/apply_info/<int:event_apply_sn>", methods=["GET"])
def get_event_apply_info(event_apply_sn):
    manager = apply.Manager()
    event_apply_info = manager.get_event_apply_info(event_apply_sn)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=event_apply_info, info=info)


@api.route("/event/<int:event_basic_sn>/apply_info", methods=["GET"])
def get_event_apply_info_by_event_basic_sn(event_basic_sn):
    manager = apply.Manager()
    event_apply_info = manager.get_event_apply_info_by_event_basic_sn(event_basic_sn)

    info = {
        "code": OK.code,
        "message": OK.message
    }

    return jsonify(data=event_apply_info, info=info)
