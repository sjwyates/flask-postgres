from sqlalchemy.types import Enum
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from flask_login import UserMixin
from portal.main.enums import ReagentStatus, ExpiryTypes, ContainerUnits
from portal import db


class BaseMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class PortalUser(UserMixin, db.Model):
    __tablename__ = 'portaluser'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    given_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    auth_level = db.Column(Enum('Admin', 'Super', 'Normal', name='auth_level'))
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class Reagent(BaseMixin, db.Model):

    template_id = db.Column(db.Integer, db.ForeignKey('reagenttemplate.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'))
    status = db.Column(Enum(ReagentStatus))

    def __init__(self, template_id, lot_id, expiry, status):
        self.template_id = template_id
        self.lot_id = lot_id
        self.expiry = expiry
        self.status = ReagentStatus[status]

    def __repr__(self):
        return '<Reagent #%r>' % self.id


class ReagentTemplate(BaseMixin, db.Model):

    description = db.Column(db.String(50))
    expiry_dur = db.Column(db.Integer, default=0)
    expiry_type = db.Column(Enum(ExpiryTypes))
    container_size = db.Column(db.Float)
    container_units = db.Column(Enum(ContainerUnits))
    requires_qual = db.Column(db.Boolean, default=False)
    reorder_qty = db.Column(db.Integer)
    reorder_trigger = db.Column(db.Integer)
    cas = db.Column(db.String(20))
    ghs = db.Column(db.Integer)
    reagents = db.relationship('Reagent', backref='template', lazy=True)
    lots = db.relationship('Lot', backref='template', lazy=True)

    def __init__(self, description, expiry_dur, expiry_type,
                 container_size, container_units, requires_qual,
                 reorder_qty, reorder_trigger, cas, ghs):
        self.description = description
        self.expiry_dur = expiry_dur
        self.expiry_type = ExpiryTypes[expiry_type]
        self.container_size = container_size
        self.container_units = ContainerUnits[container_units]
        self.requires_qual = requires_qual
        self.reorder_qty = reorder_qty
        self.reorder_trigger = reorder_trigger
        self.cas = cas
        self.ghs = ghs

    def __repr__(self):
        return '<Template #%r>' % self.id


class Lot(BaseMixin, db.Model):

    template_id = db.Column(db.Integer, db.ForeignKey('reagenttemplate.id'))
    mfg_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
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
