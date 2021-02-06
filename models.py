
#
#
# class ReagentTemplate(db.Model):
#     template_id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(50), nullable=False)
#     expiry_dur = db.Column(db.Integer, nullable=False, default=0)
#     expiry_type = db.Column(db.String(10), nullable=False, default='N/A')
#     container_size = db.Column(db.Float, nullable=False)
#     container_units = db.Column(db.String(10), nullable=False)
#     requires_qual = db.Column(db.Boolean, nullable=False, default=False)
#
#     def __repr__(self):
#         return '<Template #%r>' % self.template_id
#
#
# class Lot(db.Model):
#     lot_id = db.Column(db.Integer, primary_key=True)
#     mfg_id = db.Column(db.Integer, nullable=False)
#     lot_num = db.Column(db.String(30), nullable=False, default=False)
#     expiry = db.Column(db.DateTime, nullable=False)
#
#     def __repr__(self):
#         return '<Lot #%r>' % self.lot_id
#
#
# class Manufacturer(db.Model):
#     mfg_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#
#     def __repr__(self):
#         return '<Manfucaturer #%r>' % self.lot_id
