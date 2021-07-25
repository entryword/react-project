from flask import request, session
from flask_login import current_user

from app.constant import UserType
from app.utils import login_required, json_response, permit_params
from . import api
from ..managers.member import Manager as MemberManager


@api.route('/member/me', methods=['GET'])
@login_required(user_type=UserType.MEMBER)
def get_member():
    member = MemberManager.get_member(current_user.id)
    member['first_time_login'] = session['first_time_login']

    if session['first_time_login']:
        session['first_time_login'] = False

    return json_response(member)


@api.route('/member/me', methods=['PUT'])
@login_required(user_type=UserType.MEMBER)
def update_member():
    user_id = current_user.id
    member_data = permit_params(request.get_json(), ['name', 'is_student', 'title', 'fields'])

    MemberManager.update_member(user_id, member_data)

    return json_response({'id': user_id})
