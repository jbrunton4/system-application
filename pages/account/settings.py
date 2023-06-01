from __main__ import app
import flask
from zenora import APIClient


@app.route("/account/settings", methods=["GET"])
def settings() -> flask.Response:

    # ensure that the user is logged in
    if "token" in flask.session:
        bearer_client = APIClient(flask.session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return flask.make_response(flask.render_template("account/settings.html", current_user=current_user))

