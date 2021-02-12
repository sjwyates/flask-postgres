# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Portal Login')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Username as password do not match')
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember=True)
            return redirect(url_for('main.dashboard'))
