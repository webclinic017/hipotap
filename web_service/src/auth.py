from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests

API_GATEWAY_URL = "http://hipotap_api_gateway:8000"
AUTHENTICATE_ENDPOINT = f"{API_GATEWAY_URL}/customer/authenticate/"

auth = Blueprint('auth', __name__)



@auth.get('/login')
def login():
    return render_template('login.html')

@auth.post('/login')
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # call to API Gateway for authentication
    response = requests.post(AUTHENTICATE_ENDPOINT, data={'email':email, 'password':password})

    if response.status_code != 200:
        flash('Invalid credentials', 'is-danger')
        return redirect(url_for('auth.login'))

    customer_data = response.json()
    session['username'] = customer_data['name']
    # return reply
    return redirect(url_for('main.profile'))

@auth.get('/signup')
def signup():
    return render_template('signup.html')

@auth.post('/signup')
def signup_post():
    # register user
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    # redirect to login
    return redirect(url_for('auth.login'))

@auth.post('/logout')
def logout():
    flash("Logged out", "is-info")
    return redirect(url_for('main.index'))
