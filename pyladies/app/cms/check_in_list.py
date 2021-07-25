from flask import jsonify, request

from app.exceptions import OK
from app.managers.check_in_list import CheckInListManager
from app.schemas.check_in_list_info import create_schema, update_schema
from app.utils import login_required, payload_validator
from . import api


@api.route('/check-in-list/upload/<int:event_basic_id>', methods=["POST"])
@login_required
def upload_check_in_list(event_basic_id):
    files = request.files.getlist('files')
    data = CheckInListManager.upload(event_basic_sn=event_basic_id, files=files)
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
        'event_basic_sn': payload['event_basic_id'],
        'name': payload['name'],
        'mail': payload['mail'],
        'phone': payload['phone'],
        'ticket_type': payload['ticket_type'],
        'ticket_amount': payload['ticket_amount'],
        'remark': payload['remark'],
        'status': payload['status']
    }
    sn = CheckInListManager.create_check_in_list(info=info)
    data = {
        "id": sn
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/check-in-list/event/<int:event_basic_id>", methods=["GET"])
@login_required
def get_check_in_list_by_event_basic_sn(event_basic_id):
    data = CheckInListManager.get_check_in_list(event_basic_sn=event_basic_id)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/check-in-list/<int:check_in_list_id>", methods=["PUT"])
@login_required
@payload_validator(update_schema)
def update_check_in_list(check_in_list_id, payload):
    CheckInListManager.update_check_in_list(
        check_in_list_sn=check_in_list_id,
        info=payload
    )
    data = {
        "id": check_in_list_id
    }
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(data=data, info=info)


@api.route("/check-in-list/<int:check_in_list_id>", methods=["DELETE"])
@login_required
def delete_check_in_list(check_in_list_id):
    CheckInListManager.delete_check_in_list(check_in_list_sn=check_in_list_id)
    info = {
        "code": OK.code,
        "message": OK.message
    }
    return jsonify(info=info)
