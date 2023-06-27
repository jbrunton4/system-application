from __main__ import app
import flask
from zenora import APIClient
from models import alter


@app.route("/account/alter/edit", methods=["GET", "POST"])
def edit_alter() -> flask.Response:
    if "token" not in flask.session:
        return flask.make_response(flask.redirect("auth/discord"))

    # get the current alter from the discord rest API
    bearer_client = APIClient(flask.session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()

    # get the alter in question
    a = alter.Alter(flask.request.args.get("id"))
    # @todo: 404 if alter not found. Find how to raise HTTP error in Flask. maybe return flask.error(404)?

    # handle post request to make new alter
    if flask.request.method == "POST":

        a.name = flask.request.form.get("name") or ""
        a.description = flask.request.form.get("description") or ""
        a.pronouns = flask.request.form.get("pronouns") or ""
        a.age = flask.request.form.get("age") or ""
        a.auto_age = bool(flask.request.form.get("auto_age"))
        a.roles = flask.request.form.get("roles") or ""
        a.profile_picture_url = flask.request.form.get("profile_picture_url") or ""
        a.start_tag = flask.request.form.get("start_tag") or ""
        a.end_tag = flask.request.form.get("end_tag") or ""
        a.save()

    return flask.make_response(flask.render_template("account/alter/edit.html",
                                                     current_user=current_user or "",
                                                     name=a.name or "",
                                                     description=a.description or "",
                                                     pronouns=a.pronouns or "",
                                                     age=a.age or "",
                                                     auto_age=str(int(a.auto_age)),
                                                     roles=a.roles or "",
                                                     profile_picture_url=a.profile_picture_url or "",
                                                     start_tag=a.start_tag or "",
                                                     end_tag=a.end_tag or ""))
