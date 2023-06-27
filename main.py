from flask import *
from zenora import APIClient

# Initialise an app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "beeeansbones"

# Initialise the Zenora client for discord REST API rquests
with open("config.json", "r") as fh:
    data = json.load(fh)
    client_id = data["discordClientId"]
    client_secret = data["discordClientSecret"]
    client_token = data["discordApplicationToken"]
zenora_client = APIClient(client_token)

from pages.auth import discord
from pages.account import dashboard, settings, closure_confirmation
from pages.account.alter import create, edit, view
from pages import about


@app.route("/", methods=["GET"])
def index():
    return make_response(render_template("index.html"))


app.run(host="0.0.0.0", port=81, debug=True)
