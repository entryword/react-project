from flask import current_app, redirect, session, url_for, request

from app.constant import UserType
from app.utils import login_required
from . import api
from ..managers.member import Manager as MemberManager


@api.route('/login', methods=['GET'])
def login():
    redirect_uri = url_for('api.auth', _external=True)
    return current_app.oauth.google.authorize_redirect(redirect_uri)


@api.route('/auth', methods=['GET'])
def auth():
    if current_app.config['TESTING']:
        user_info = {
            'email': request.args.get('email'),
            'name': request.args.get('name')
        }
    else:
        google = current_app.oauth.google
        google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()

    session['user_type'] = UserType.MEMBER
    new_created = MemberManager.social_login(user_info['email'], user_info['name'])
    session['first_time_login'] = new_created
    return redirect('/')


@api.route('/logout', methods=['GET'])
@login_required(user_type=UserType.MEMBER)
def logout():
    MemberManager.logout()
    return redirect('/')
