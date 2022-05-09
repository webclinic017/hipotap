from flask import Blueprint, render_template, session

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", session=session)


@main.route("/profile")
def profile():
    return render_template("profile.html", username=session)
