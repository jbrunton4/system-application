from __main__ import app, zenora_client
import flask
import json
from zenora import APIClient


@app.route("/account/welcome", methods=["GET"])
def welcome() -> flask.Response:

    if "token" in flask.session:

        # get the current alter from the discord rest API
        bearer_client = APIClient(flask.session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()

        return flask.make_response(flask.render_template("account/welcome.html", current_user=current_user))
