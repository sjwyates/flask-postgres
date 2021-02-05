from app import db


class Reagent(db.Model):
    __tablename__ = 'reagents'

    id = db.Column(db.Integer, primary_key=True)
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


class ReagentTemplate(db.Model):
    __tablename__ = 'reagent_templates'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    expiry_dur = db.Column(db.Integer, nullable=False, default=0)
    expiry_type = db.Column(db.String(10), nullable=False, default='N/A')
    container_size = db.Column(db.Float, nullable=False)
    container_units = db.Column(db.String(10), nullable=False)
    requires_qual = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, description, expiry_duration, expiry_type, container_size, container_units, requires_qual):
        self.description = description
        self.expiry_dur = expiry_duration
        self.expiry_type = expiry_type
        self.container_size = container_size
        self.container_units = container_units
        self.requires_qual = requires_qual

    def __repr__(self):
        return '<Template #%r>' % self.template_id


class Lot(db.Model):
    __tablename__ = 'lots'

    id = db.Column(db.Integer, primary_key=True)
    mfg_id = db.Column(db.Integer, nullable=False)
    lot_num = db.Column(db.String(30), nullable=False, default=False)
    expiry = db.Column(db.DateTime, nullable=False, default='NA')
    cofa = db.Column(db.String(50), nullable=False)

    def __init__(self, mfg_id, lot_num, expiry, cofa):
        self.mfg_id = mfg_id
        self.lot_num = lot_num
        self.expiry = expiry
        self.cofa = cofa

    def __repr__(self):
        return '<Lot #%r>' % self.lot_id


class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Manfucaturer #%r>' % self.mfg_id
