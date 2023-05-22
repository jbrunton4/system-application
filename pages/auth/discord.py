from __main__ import app
import flask
import json
from zenora import APIClient

# load the client ID and secret from config
with open("config.json", "r") as fh:
    data = json.load(fh)
    client_id = data["discordClientId"]
    client_secret = data["discordClientSecret"]
    client_token = data["discordApplicationToken"]

# initialize the Zenora API client
zenora_client = APIClient(client_token, client_secret=client_secret)


@app.route("/auth/discord", methods=["GET"])
def auth_discord() -> flask.Response:
    # grab the access code from the query string
    # Trying to get the token directly can cause issues here as the URL discord sends us uses # instead of ?
    # to begin the query string. The method used here takes longer, but is necessary until a fix is found.
    code = flask.request.args.get("code", None)

    # send a request for data to the discord API
    if code is not None:
        access_token = zenora_client.oauth.get_access_token(code, "http://127.0.0.1:81/auth/discord").access_token
        print(access_token)
        flask.session["token"] = access_token
        return flask.make_response(flask.redirect("/account/dashboard"))

    return flask.make_response(flask.render_template("account/errors/not-logged-in.html"))
