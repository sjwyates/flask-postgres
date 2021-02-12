from sqlalchemy.types import Enum
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db


class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class User(UserMixin, db.Model):

    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))
    given_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))


class Reagent(BaseMixin, db.Model):

    template_id = db.Column(db.Integer, db.ForeignKey('reagent_templates.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))
    status = db.Column(Enum('Unopened', 'Open', 'Quarantine', 'Discarded', name='status'))

    def __init__(self, template_id, lot_id, expiry, status):
        self.template_id = template_id
        self.lot_id = lot_id
        self.expiry = expiry
        self.status = status

    def __repr__(self):
        return '<Reagent #%r>' % self.id


class ReagentTemplate(BaseMixin, db.Model):

    description = db.Column(db.String(50))
    expiry_dur = db.Column(db.Integer, default=0)
    expiry_type = db.Column(Enum('single use', 'hours', 'days', 'weeks', 'months', 'years',
                                 name='expiry_types'))
    container_size = db.Column(db.Float)
    container_units = db.Column(Enum('L', 'mL', 'uL', 'kg', 'g', 'mg', 'ug', 'ga', 'oz', 'vials', 'kits', 'units',
                                     name='container_units'))
    requires_qual = db.Column(db.Boolean, default=False)
    reorder_qty = db.Column(db.Integer)
    reorder_trigger = db.Column(db.Integer)
    cas = db.Column(db.String(20))
    ghs = db.Column(db.Integer)
    reagents = db.relationship('Reagent', backref='template', lazy=True)
    lots = db.relationship('Lot', backref='template', lazy=True)

    def __init__(self, description, expiry_duration, expiry_type,
                 container_size, container_units, requires_qual,
                 reorder_qty, reorder_trigger, cas, ghs):
        self.description = description
        self.expiry_dur = expiry_duration
        self.expiry_type = expiry_type
        self.container_size = container_size
        self.container_units = container_units
        self.requires_qual = requires_qual
        self.reorder_qty = reorder_qty
        self.reorder_trigger = reorder_trigger
        self.cas = cas
        self.ghs = ghs

    def __repr__(self):
        return '<Template #%r>' % self.id


class Lot(BaseMixin, db.Model):

    template_id = db.Column(db.Integer, db.ForeignKey('reagent_templates.id'))
    mfg_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    lot_num = db.Column(db.String(30), default=False)
    expiry = db.Column(db.DateTime, default='NA')
    cofa = db.Column(db.String(50))
    reagents = db.relationship('Reagent', backref='lot', lazy=True)

    def __init__(self, template_id, mfg_id, lot_num, expiry):
        self.template_id = template_id
        self.mfg_id = mfg_id
        self.lot_num = lot_num
        self.expiry = expiry
        self.cofa = f"path/to/cofas/{mfg_id}-{lot_num}.pdf"

    def __repr__(self):
        return '<Lot #%r>' % self.id


class Manufacturer(BaseMixin, db.Model):

    name = db.Column(db.String(20))
    lots = db.relationship('Lot', backref='manufacturer', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Manufacturer #%r>' % self.id
