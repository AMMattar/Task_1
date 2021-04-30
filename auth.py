from flask import Blueprint, render_template, redirect, url_for, Flask

auth = Blueprint('auth', __name__)
app=Flask(__name__)

# @app.route('/login', methods=["POST", "GET"])
# def login_post():
#    render_template('profile.html')

