# from app import app
from flask import Blueprint, render_template, session
# from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', session=session)

@main.route('/profile')
def profile():
    return render_template('profile.html', username=session)
