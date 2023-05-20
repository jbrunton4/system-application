from flask import *

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "beeeansbones"

from pages.auth import discord
from pages.account import dashboard
from pages import about


@app.route("/", methods=["GET"])
def index():
    return make_response(render_template("index.html"))


app.run(host="0.0.0.0", port=81, debug=True)
