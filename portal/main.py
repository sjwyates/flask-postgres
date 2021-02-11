from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('views/index.html', title='Home')


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('views/dashboard.html',
                           title='Dashboard',
                           given_name=current_user.given_name,
                           surname=current_user.surname)
