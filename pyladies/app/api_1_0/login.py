from authlib.integrations.flask_client import OAuth
from flask import current_app, jsonify, redirect, session, url_for

from . import api
from ..exceptions import OK

@api.route("/login", methods=["GET"])
def login():
    redirect_uri = url_for('api.auth', _external=True)
    return current_app.oauth.google.authorize_redirect(redirect_uri)

@api.route("/auth", methods=["GET"])
def auth():
    google = current_app.oauth.google
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    session['user'] = user_info
    session.permanent = True # flask sessions expire once you close the browser unless you have a permanent session
    return redirect('/')

@api.route("/logout", methods=["GET"])
def logout():
    session.pop('user', None)
    return redirect('/')

@api.route("/user", methods=["GET"])
def user():
    user_info = session.get('user') or {}
    info = {"code": OK.code, "message": OK.message}
    return jsonify(data=user_info, info=info)
