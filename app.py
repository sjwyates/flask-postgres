from flask import Flask, render_template, request
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
    return render_template('index.html')


@app.route('/reagent', methods=['GET', 'POST'])
def reagents():
    errors = []
    if request.method == "POST":
        try:
            template = Lot(
                mfg_id='1',
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
    return render_template('reagent.html')


if __name__ == '__main__':
    app.run()
