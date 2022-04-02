from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
# from . import db

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
    reply = requests.get(f"http://hipotap_api_gateway:8000/customer/authenticate/?email={email}&password={password}").json()
    session['username'] = reply['reply']
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
    return 'Logout'

# from functools import wraps
# from flask import g, abort



# def restricted(access_level):
#     def decorator(func):
#         # @wraps(func)
#         def wrapper(*args, **kwargs):
#             if not g.user.access_level == access_level:
#                 abort(403)
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator
