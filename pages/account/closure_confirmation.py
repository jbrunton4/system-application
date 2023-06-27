from __main__ import app
import flask
from zenora import APIClient
from secrets import token_urlsafe
from models.user import User


@app.route("/account/closure-confirmation", methods=["GET"])
def closure_confirmation() -> flask.Response:

    # ensure that the alter is logged in
    if "token" in flask.session:
        bearer_client = APIClient(flask.session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
    else:
        return flask.make_response(flask.redirect("/"))

    if flask.request.method == "POST":

        if flask.request.form["verification_code"] == flask.request.form["correct_verification_code"]:
            user_object = User(str(current_user.id))
            user_object.delete()
            return flask.make_response(flask.redirect("/"))
        else:
            return flask.make_response(flask.render_template("account/closure-confirmation.html",
                                                             status="Incorrect code, please try again.",
                                                             current_user=current_user,
                                                             verification_code=token_urlsafe(4)))

    return flask.make_response(flask.render_template("account/closure-confirmation.html",
                                                     status="",
                                                     current_user=current_user,
                                                     verification_code=token_urlsafe(4)))