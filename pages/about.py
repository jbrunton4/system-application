from __main__ import app
import flask
import json


@app.route("/about", methods=["GET"])
def about() -> flask.Response:

    return flask.make_response(flask.render_template("about.html") )
