# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)
from .models import ReagentTemplate, Lot, Manufacturer
# from seed import manufacturers, reagent_templates, lots, reagents


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('views/login.html', title='Portal Login')
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


@auth.route('/reagents/add', methods=['GET', 'POST'])
def add_reagent():
    if request.method == 'GET':
        templates = [{
            'id': getattr(d, 'id'),
            'description': getattr(d, 'description'),
            'container_size': getattr(d, 'container_size'),
            'container_units': getattr(d, 'container_units'),
            'requires_qual': getattr(d, 'requires_qual')
        } for d in db.session.query(ReagentTemplate).all()]
        mfgs = [{
            'id': getattr(d, 'id'),
            'name': getattr(d, 'name')
        } for d in db.session.query(Manufacturer).all()]
        lots = [{
            'id': getattr(d, 'id'),
            'lot_num': getattr(d, 'lot_num'),
            'template_id': getattr(d, 'template_id'),
            'mfg_id': getattr(d, 'mfg_id'),
            'expiry': getattr(d, 'expiry')
        } for d in db.session.query(Lot).all()]
        return render_template('views/add-reagent.html',
                               templates=templates,
                               manufacturers=mfgs,
                               lots=lots,
                               title='Reagent Receipt')
    if request.method == 'POST':
        headers = request.headers
        print(dict(request.headers))
        return 'gneiss!'
        # return redirect(url_for('details', reagent_id=reagent['template_id']))


@auth.route('/reagents/<reagent_id>', methods=['GET'])
def details(reagent_id):
    return render_template('views/reagent-details.html', title='Reagent Details', reagent_id=reagent_id)


# @auth.route('/reagents/s33d/<table>', methods=['POST'])
# def seed(table):
#     if table == 'all':
#         db.create_all()
#     elif table == 'mfg':
#         for mfg in manufacturers:
#             entry = Manufacturer(
#                 name=mfg
#             )
#             db.session.add(entry)
#             db.session.commit()
#     elif table == 'temp':
#         for temp in reagent_templates:
#             entry = ReagentTemplate(
#                 description=temp['description'],
#                 expiry_duration=temp['expiry_dur'],
#                 expiry_type=temp['expiry_type'],
#                 container_size=temp['container_size'],
#                 container_units=temp['container_units'],
#                 requires_qual=temp['requires_qual']
#             )
#             db.session.add(entry)
#             db.session.commit()
#     elif table == 'lot':
#         for lot in lots:
#             entry = Lot(
#                 template_id=lot['temp_id'],
#                 mfg_id=lot['mfg_id'],
#                 lot_num=lot['lot_num'],
#                 expiry=lot['expiry']
#             )
#             db.session.add(entry)
#             db.session.commit()
#     elif table == 'reagent':
#         for reagent in reagents:
#             entry = Reagent(
#                 template_id=reagent['template_id'],
#                 lot_id=reagent['lot_id'],
#                 expiry=reagent['expiry'],
#                 status=reagent['status']
#             )
#             db.session.add(entry)
#             db.session.commit()
#     return 'Good times!'


if __name__ == '__main__':
    auth.run()
