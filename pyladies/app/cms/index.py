from . import api


@api.route("/hello/<name>", methods=["GET"])
def hello(name):
    return "Hi, {}".format(name)
