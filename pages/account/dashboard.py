from __main__ import app
import flask
import json
from zenora import APIClient
from models import user


@app.route("/account/dashboard", methods=["GET"])
def dashboard() -> flask.Response:

    if "token" in flask.session:

        # get the current alter from the discord rest API
        bearer_client = APIClient(flask.session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()

        # if the current alter isn't already a signed up member, create a system
        if not user.exists(str(current_user.id)):
            u = user.new(str(current_user.id))
            u.system_name = current_user.username
            u.profile_picture_url = current_user.avatar_url
            return flask.make_response(flask.redirect("/welcome"))

        # @todo: Change edit system button to redir to member list with edit and delete buttons

        return flask.make_response(flask.render_template("account/dashboard.html", current_user=current_user))
