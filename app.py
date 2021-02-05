from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sassutils.wsgi import SassMiddleware
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/scss', 'static/css', '/static/css')
})
db = SQLAlchemy(app)

from models import Reagent, ReagentTemplate, Lot, Manufacturer


@app.route('/', methods=['GET', 'POST'])
def home():
    results = db.session.query(Manufacturer)
    return render_template('views/index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_reagent():
    if request.method == 'GET':
        manufacturers = [{
            'id': getattr(d, 'id'),
            'name': getattr(d, 'name')
        } for d in db.session.query(Manufacturer).all()]
        templates = [{
            'id': getattr(d, 'id'),
            'description': getattr(d, 'description')
        } for d in db.session.query(ReagentTemplate).all()]
        lots = [{
            'id': getattr(d, 'id'),
            'lot_num': getattr(d, 'lot_num')
        } for d in db.session.query(Lot).all()]
        return render_template('views/add-reagent.html',
                               manufacturers=manufacturers,
                               templates=templates,
                               lots=lots)


@app.route('/reagent', methods=['GET', 'POST'])
def reagents():
    errors = []
    if request.method == "POST":
        try:
            template = Lot(
                temp_id=2,
                mfg_id=4,
                lot_num='abc123',
                expiry=datetime(2022, 11, 4, 0, 0),
                cofa='path/to/file/cofa.pdf'
            )
            db.session.add(template)
            db.session.commit()
        except:
            errors.append(
                f"Problem: could not add {request.json['name']}"
            )
    return render_template('views/reagent-details.html')


if __name__ == '__main__':
    app.run()
