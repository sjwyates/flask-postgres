from app import db
from enums import UnitsOfMeasure, ExpiryTypes, ReagentStatus


class Reagent(db.Model):
    __tablename__ = 'reagents'

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('reagent_templates.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))
    status = db.Column(db.Enum(ReagentStatus), default=ReagentStatus.U)

    def __init__(self, template_id, lot_id, expiry):
        self.template_id = template_id
        self.lot_id = lot_id
        self.expiry = expiry
        self.status = ReagentStatus.U

    def __repr__(self):
        return '<Reagent #%r>' % self.id


class ReagentTemplate(db.Model):
    __tablename__ = 'reagent_templates'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    expiry_dur = db.Column(db.Integer, default=0)
    expiry_type = db.Column(db.Enum(ExpiryTypes))
    container_size = db.Column(db.Float)
    container_units = db.Column(db.Enum(UnitsOfMeasure))
    requires_qual = db.Column(db.Boolean, default=False)
    reagents = db.relationship('Reagent', backref='template', lazy=True)
    reagents = db.relationship('Lot', backref='template', lazy=True)

    def __init__(self, description, expiry_duration, expiry_type, container_size, container_units, requires_qual):
        self.description = description
        self.expiry_dur = expiry_duration
        self.expiry_type = expiry_type
        self.container_size = container_size
        self.container_units = container_units
        self.requires_qual = requires_qual

    def __repr__(self):
        return '<Template #%r>' % self.id


class Lot(db.Model):
    __tablename__ = 'lots'

    id = db.Column(db.Integer, primary_key=True)
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


class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    lots = db.relationship('Lot', backref='manufacturer', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Manufacturer #%r>' % self.id