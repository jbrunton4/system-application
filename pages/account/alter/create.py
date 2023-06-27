from __main__ import app, zenora_client
import flask
import json
from zenora import APIClient
from models import user


@app.route("/account/alter/create", methods=["GET", "POST"])
def create_alter() -> flask.Response:

    if "token" not in flask.session:
        return flask.make_response(flask.redirect("auth/discord"))


    # get the current alter from the discord rest API
    bearer_client = APIClient(flask.session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()

    # handle post request to make new alter
    if flask.request.method == "POST":
        new_alter = user.User(str(current_user.id)).create_alter(flask.request.form["new_alter_name"])
        return flask.make_response(flask.redirect(f"/account/alter/edit?id={new_alter.get_uuid()}"))

    return flask.make_response(flask.render_template("account/alter/create.html", current_user=current_user))

    # @todo: Link to this on edit page. Auto populate name field and redir to edit.