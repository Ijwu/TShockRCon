from flask import render_template, request, redirect, url_for, flash, session
from TShockRCon import app
from TShockRCon.config import get_config_value
from TShockRCon.exceptions import ConfigOptionInvalidException
from TShockRCon.utils import terraria_to_24h
from pyshock import TShock
from pyshock.exceptions import ApiException

name = get_config_value("NAME")
ip = get_config_value("IP")
port = get_config_value("PORT")
try:
    port = int(port)
except ValueError:
    raise ConfigOptionInvalidException("SERVER.PORT", port)
server = TShock(ip, port)

@app.route("/")
def index():
    if session["logged_in"]:
        return redirect(url_for("status"))
    return render_template("index.html", server_name=name)

@app.route("/", methods=["POST"])
def index_login():
    user = request.form["username"]
    password = request.form["password"]
    try:
        server.get_token(user, password)
    except ApiException as e:
        flash(e.args[0], "error")
        return redirect(url_for("index"))
    else:
        session["username"] = user
        session["logged_in"] = True
        return redirect(url_for("status"))

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("index"))

@app.route("/status")
def status():
    if not session["logged_in"]:
        flash("You are not logged in. Please log in.", "notice")
        return redirect(url_for("index"))
    user = session["username"]
    try:
        world_info = server.get_world_info()
        server_info = server.get_server_status_v2(players=True)
    except ApiException:
        session["logged_in"] = False
        flash("You are not logged in. Please log in.", "notice")
        return redirect(url_for("index"))
    status_info = dict(user_name=user,
                       world_name=world_info["name"],
                       world_size=world_info["size"],
                       world_time=terraria_to_24h(
                           world_info["time"],
                           not bool(world_info["daytime"])),
                       world_bloodmoon=world_info["bloodmoon"],
                       world_invasion=world_info["invasionsize"],
                       players=server_info['players'],
                       server_name=name,
                       check_login=True)
    return render_template("status.html", **status_info)


@app.route("/console")
def console():
    if not session["logged_in"]:
        flash("You are not logged in. Please log in.", "notice")
        return redirect(url_for("index"))
    return render_template("console.html")