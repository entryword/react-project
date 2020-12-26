from flask import jsonify
from flask_login import login_required

from app.cms import api
from app.exceptions import OK
from app.managers.check_in_list import CheckInListManager


@api.route("/check-in-list/<int:event_basic_sn>", methods=["GET"])
@login_required
def get_check_in_list(event_basic_sn):
    data = CheckInListManager.get_check_in_list(event_basic_sn=event_basic_sn)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/check-in-list", methods=["PUT"])
@login_required
def update_check_in_list(payload):
    """
        TODO add payload validator
    """
    update_attr = dict()
    if 'status' in payload:
        update_attr.update({
            'status': payload['status']
        })
    if 'remark' in payload:
        update_attr.update({
            'remark': payload['remark']
        })
    data = CheckInListManager.update_check_in_list(
        event_basic_sn=payload['event_basic_sn'],
        user_sn=payload['event_basic_sn'],
        info=update_attr
    )
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/check-in-list/<int:check_in_list_sn>", methods=["DELETE"])
@login_required
def delete_check_in_list(check_in_list_sn):
    CheckInListManager.delete_check_in_list(check_in_list_sn=check_in_list_sn)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)
