from __main__ import app
import flask
import requests
import json
from zenora import APIClient

# load the client ID and secret from config
with open("config.json", "r") as fh:
    data = json.load(fh)
    client_id = data["discordClientId"]
    client_secret = data["discordClientSecret"]
    client_token = data["discordApplicationToken"]

# initialize the Zenora API client
zenora_client = APIClient(client_token)


@app.route("/dashboard", methods=["GET"])
def dashboard() -> flask.Response:

    if "token" in flask.session:
        bearer_client = APIClient(flask.session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return flask.make_response(flask.render_template("account/dashboard.html", user=current_user))
