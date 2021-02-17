# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import PortalUser

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Portal Login')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = PortalUser.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Username as password do not match')
            return redirect(url_for('auth.login'))
        else:
            login_user(user, remember=False)
            return redirect(url_for('main.dashboard'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
        given_name = request.form.get('given_name')
        surname = request.form.get('surname')
        username = request.form.get('username')
        password = request.form.get('password')
        auth_level = 'Super'

        user = PortalUser.query.filter_by(
            username=username).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Username already exists')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = PortalUser(given_name=given_name, surname=surname, username=username, auth_level=auth_level,
                              password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    elif request.method == 'GET':
        return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))