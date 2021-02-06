from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sassutils.wsgi import SassMiddleware
import os
from seed import manufacturers, reagent_templates, lots, reagents

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


@app.route('/seed', methods=['POST'])
def seed():
    db.create_all()
    for mfg in manufacturers:
        entry = Manufacturer(
            name=mfg
        )
        db.session.add(entry)
    for temp in reagent_templates:
        entry = ReagentTemplate(
            description=temp['description'],
            expiry_duration=temp['expiry_dur'],
            expiry_type=temp['expiry_type'],
            container_size=temp['container_size'],
            container_units=temp['container_units'],
            requires_qual=temp['requires_qual']
        )
        db.session.add(entry)
    for lot in lots:
        entry = Lot(
            template_id=lot['temp_id'],
            mfg_id=lot['mfg_id'],
            lot_num=lot['lot_num'],
            expiry=lot['expiry']
        )
        db.session.add(entry)
    for reagent in reagents:
        entry = Reagent(
            template_id=reagent['template_id'],
            lot_id=reagent['lot_id'],
            expiry=reagent['expiry']
        )
        db.session.add(entry)
    db.session.commit()
    return 'Good times!'


if __name__ == '__main__':
    app.run()
