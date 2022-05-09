from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from ..session.auth import (
    login_user,
    logout_user,
    signup_user,
    UserAlreadyExistsException,
)

API_GATEWAY_URL = "http://hipotap_api_gateway:8000"
AUTHENTICATE_ENDPOINT = f"{API_GATEWAY_URL}/customer/authenticate/"

auth = Blueprint("auth", __name__)


@auth.get("/login")
def login():
    return render_template("login.html", session=session)


@auth.post("/login")
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        login_user(email, password)
    except:
        flash("Invalid credentials", "is-danger")
        return redirect(url_for("auth.login"))

    return redirect(url_for("main.profile"))


@auth.get("/signup")
def signup():
    return render_template("signup.html", session=session)


@auth.post("/signup")
def signup_post():
    # register user
    email = request.form.get("email")
    name = request.form.get("name")
    surname = request.form.get("surname")
    password = request.form.get("password")
    try:
        signup_user(name, surname, email, password)
    except UserAlreadyExistsException:
        flash("Email is taken", "is-danger")
        return redirect(url_for("auth.signup"))

    # redirect to login
    flash("Account created!", "is-success")
    return redirect(url_for("auth.login"))


@auth.post("/logout")
def logout():
    logout_user()
    flash("Logged out", "is-info")
    return redirect(url_for("main.index"))
