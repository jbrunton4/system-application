from __main__ import app, zenora_client
import flask
import json
from zenora import APIClient
from models import alter


@app.route("/alter/<id>")
@app.route("/account/alter/<id>", methods=["GET"])
def view_alter(**kwargs) -> flask.Response:

    if "token" not in flask.session:
        return flask.make_response(flask.redirect("auth/discord"))


    # get the current alter from the discord rest API
    bearer_client = APIClient(flask.session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()

    # get alter
    a = alter.Alter(kwargs["id"])

    # display the alter info
    return flask.make_response(flask.render_template("account/alter/view.html",
                                                     current_user=current_user,
                                                     alter=a))

    # @todo: Link to this on edit page. Auto populate name field and redir to edit.