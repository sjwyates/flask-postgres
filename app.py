import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Reagent(db.Model):
    __tablename__ = 'reagents'

    reagent_id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, nullable=False)
    lot_id = db.Column(db.Integer, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __init__(self, template_id, lot_id, expiry, status="unopened"):
        self.template_id = template_id
        self.lot_id = lot_id
        self.expiry = expiry
        self.status = status

    def __repr__(self):
        return '<Reagent #%r>' % self.reagent_id


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/add', methods=["POST"])
# def add_reagent():
#     in_data = DataEntry(request.form['mydata'])
#     data = copy(indata.__dict__)
#     del data["_sa_instance_state"]
#     try:
#         db.session.add(indata)
#         db.session.commit()
#     except Exception as e:
#         print("\n FAILED entry: {}\n".format(json.dumps(data)))
#         print(e)
#         sys.stdout.flush()
#     return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))


if __name__ == '__main__':
    app.run()
