from flask import jsonify, request
from flask_login import login_required

from app.exceptions import OK
from app.managers.check_in_list import CheckInListManager
from app.schemas.check_in_list_info import create_schema, update_schema
from app.utils import payload_validator
from . import api


@api.route('/check-in-list/upload/<int:event_basic_sn>', methods=["POST"])
def upload_check_in_list(event_basic_sn):
    files = request.files.getlist('files')
    data = CheckInListManager.upload(event_basic_sn=event_basic_sn, files=files)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route('/check-in-list', methods=["POST"])
@login_required
@payload_validator(create_schema)
def create_check_in_list(payload):
    info = {
        'event_basic_sn': payload['event_basic_sn'],
        'user_sn': payload['user_sn'],
        'name': payload['name'],
        'mail': payload['mail'],
        'phone': payload['phone'],
        'ticket_type': payload['ticket_type'],
        'ticket_amount': payload['ticket_amount'],
        'remark': payload['remark'],
        'status': payload['status']
    }
    data = CheckInListManager.create_check_in_list(info=info)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/check-in-list/event/<int:event_basic_sn>", methods=["GET"])
@login_required
def get_check_in_list_by_event_basic_sn(event_basic_sn):
    data = CheckInListManager.get_check_in_list(event_basic_sn=event_basic_sn)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/check-in-list/<int:check_in_list_sn>", methods=["PUT"])
@login_required
@payload_validator(update_schema)
def update_check_in_list(check_in_list_sn, payload):
    CheckInListManager.update_check_in_list(
        check_in_list_sn=check_in_list_sn,
        info=payload
    )
    data = {
        "id": check_in_list_sn
    }
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
