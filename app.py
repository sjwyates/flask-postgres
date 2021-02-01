from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_heroku import Heroku
from datetime import datetime
import sys
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

engine = create_engine('postgresql+psycopg2://postgres:agcbio@localhost/reagent_portal')


class Reagent(db.Model):
    reagent_id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, nullable=False)
    lot_id = db.Column(db.Integer, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Unopened')

    def __repr__(self):
        return '<Reagent #%r>' % self.reagent_id


class ReagentTemplate(db.Model):
    template_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    expiry_dur = db.Column(db.Integer, nullable=False, default=0)
    expiry_type = db.Column(db.String(10), nullable=False, default='N/A')
    container_size = db.Column(db.Float, nullable=False)
    container_units = db.Column(db.String(10), nullable=False)
    requires_qual = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Template #%r>' % self.template_id


class Lot(db.Model):
    lot_id = db.Column(db.Integer, primary_key=True)
    mfg_id = db.Column(db.Integer, nullable=False)
    lot_num = db.Column(db.String(30), nullable=False, default=False)
    expiry = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Lot #%r>' % self.lot_id


class Manufacturer(db.Model):
    mfg_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Manfucaturer #%r>' % self.lot_id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=["POST"])
def add_reagent():
    in_data = DataEntry(request.form['mydata'])
    data = copy(indata.__dict__)
    del data["_sa_instance_state"]
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(data)))
        print(e)
        sys.stdout.flush()
    return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))


if __name__ == '__main__':
    app.run()
