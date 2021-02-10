from flask import Flask, render_template, request, json, redirect, url_for
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
    return render_template('index.html')


@app.route('/reagents/add', methods=['GET', 'POST'])
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
        return render_template('add-reagent.html',
                               templates=templates,
                               manufacturers=mfgs,
                               lots=lots)
    if request.method == 'POST':
        headers = request.headers
        print(dict(request.headers))
        return 'gneiss!'
        # return redirect(url_for('details', reagent_id=reagent['template_id']))


@app.route('/reagents/<reagent_id>', methods=['GET'])
def details(reagent_id):
    return render_template('reagent-details.html', reagent_id=reagent_id)


@app.route('/reagents/s33d/<table>', methods=['POST'])
def seed(table):
    if table == 'all':
        db.create_all()
    elif table == 'mfg':
        for mfg in manufacturers:
            entry = Manufacturer(
                name=mfg
            )
            db.session.add(entry)
            db.session.commit()
    elif table == 'temp':
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
            db.session.commit()
    elif table == 'lot':
        for lot in lots:
            entry = Lot(
                template_id=lot['temp_id'],
                mfg_id=lot['mfg_id'],
                lot_num=lot['lot_num'],
                expiry=lot['expiry']
            )
            db.session.add(entry)
            db.session.commit()
    elif table == 'reagent':
        for reagent in reagents:
            entry = Reagent(
                template_id=reagent['template_id'],
                lot_id=reagent['lot_id'],
                expiry=reagent['expiry'],
                status=reagent['status']
            )
            db.session.add(entry)
            db.session.commit()
    return 'Good times!'


if __name__ == '__main__':
    app.run()
