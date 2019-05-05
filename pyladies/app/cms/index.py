from flask_login import login_required

from . import api


@api.route("/hello/<name>", methods=["GET"])
def hello(name):
    return "Hi, {}".format(name)


@api.route("/secret", methods=["GET"])
@login_required
def secret():
    return "Only authenticated users are allowed!"
