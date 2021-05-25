from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from portal import db
import json
from portal.main.models import ReagentTemplate, Lot, Manufacturer
from portal.main.enums import EnumEncoder
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('/dashboard/'))
    else:
        return render_template('index.html', title='Home')


# @main.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html',
#                            title='Dashboard',
#                            given_name=current_user.given_name,
#                            surname=current_user.surname)


@main.route('/reagents/add', methods=['GET', 'POST'])
@login_required
def add_reagent():
    if request.method == 'GET':
        templates = json.dumps([{
            'id': getattr(d, 'id'),
            'description': getattr(d, 'description'),
            'container_size': getattr(d, 'container_size'),
            'container_units': getattr(d, 'container_units'),
            'requires_qual': getattr(d, 'requires_qual')
        } for d in db.session.query(ReagentTemplate).all()], cls=EnumEncoder)
        mfgs = json.dumps([{
            'id': getattr(d, 'id'),
            'name': getattr(d, 'name')
        } for d in db.session.query(Manufacturer).all()], cls=EnumEncoder)
        lots = json.dumps([{
            'id': getattr(d, 'id'),
            'lot_num': getattr(d, 'lot_num'),
            'template_id': getattr(d, 'template_id'),
            'mfg_id': getattr(d, 'mfg_id'),
            'expiry': datetime.strftime(getattr(d, 'expiry'), '%Y-%m-%d')
        } for d in db.session.query(Lot).all()], cls=EnumEncoder)
        return render_template('add-reagent.html',
                               templates=templates,
                               manufacturers=mfgs,
                               lots=lots,
                               title='Reagent Receipt')
    if request.method == 'POST':
        reagent = request.get_json()
        return redirect(url_for('main.details', reagent_id=reagent['lot_id']))


@main.route('/reagents/lots/add', methods=['GET', 'POST'])
@login_required
def add_lot():
    if request.method == 'GET':
        templates = json.dumps([{
            'id': getattr(d, 'id'),
            'description': getattr(d, 'description'),
            'container_size': getattr(d, 'container_size'),
            'container_units': getattr(d, 'container_units'),
            'requires_qual': getattr(d, 'requires_qual')
        } for d in db.session.query(ReagentTemplate).all()], cls=EnumEncoder)
        mfgs = json.dumps([{
            'id': getattr(d, 'id'),
            'name': getattr(d, 'name')
        } for d in db.session.query(Manufacturer).all()], cls=EnumEncoder)
        lots = json.dumps([{
            'id': getattr(d, 'id'),
            'lot_num': getattr(d, 'lot_num'),
            'template_id': getattr(d, 'template_id'),
            'mfg_id': getattr(d, 'mfg_id'),
            'expiry': datetime.strftime(getattr(d, 'expiry'), '%Y-%m-%d')
        } for d in db.session.query(Lot).all()], cls=EnumEncoder)
        return render_template('add-lot.html',
                               templates=templates,
                               manufacturers=mfgs,
                               lots=lots,
                               title='Add Reagent Lot')
    if request.method == 'POST':
        reagent = request.get_json()
        print(reagent)
        return redirect(url_for('main.add_regent'))


@main.route('/reagents/<reagent_id>', methods=['GET'])
@login_required
def details(reagent_id):
    return render_template('reagent-details.html', title='Reagent Details', reagent_id=reagent_id)


# @main.route('/reagents/s33d/<which>', methods=['GET'])
# def seed(which):
#     if which == 'mfg':
#         for item in mfgs_seed:
#             entry = Manufacturer(name=item['name'])
#             db.session.add(entry)
#             db.session.commit()
#         return 'Manufacturers added!'
#
#     elif which == 'temp':
#         for item in temps_seed:
#             entry = ReagentTemplate(
#                 description=item['description'],
#                 expiry_dur=item['expiry_dur'],
#                 expiry_type=item['expiry_type'],
#                 container_size=item['container_size'],
#                 container_units=item['container_units'],
#                 requires_qual=item['requires_qual'],
#                 reorder_qty=item['reorder_qty'],
#                 reorder_trigger=item['reorder_trigger'],
#                 cas=item['cas'],
#                 ghs=item['ghs']
#             )
#             db.session.add(entry)
#             db.session.commit()
#         return 'Templates added!'
#
#     elif which == 'lot':
#         from datetime import datetime
#         for item in lots_seed:
#             entry = Lot(
#                 template_id=int(item['template_id']),
#                 mfg_id=int(item['mfg_id']),
#                 lot_num=item['lot_num'],
#                 expiry=datetime.strptime(item['expiry'], '%m/%d/%Y')
#             )
#             db.session.add(entry)
#             db.session.commit()
#         return 'Lots added!'
#
#     else:
#         return 'Not a valid thing!'
#
#
# mfgs_seed = [{'name': 'Fisher'}, {'name': 'Sigma'}, {'name': 'VWR'}]
# temps_seed = [{'description': 'Acetic Acid', 'expiry_dur': 1, 'expiry_type': 'years', 'container_size': 500,
#                'container_units': 'mL', 'requires_qual': False, 'reorder_qty': 6, 'reorder_trigger': 2,
#                'cas': '64-19-7', 'ghs': 13},
#               {'description': 'Acetone', 'expiry_dur': 1, 'expiry_type': 'years', 'container_size': 1,
#                'container_units': 'L', 'requires_qual': False, 'reorder_qty': 6, 'reorder_trigger': 2, 'cas': '67-64-1',
#                'ghs': 27}, {'description': 'Acetonitrile', 'expiry_dur': 1, 'expiry_type': 'years', 'container_size': 4,
#                             'container_units': 'L', 'requires_qual': False, 'reorder_qty': 4, 'reorder_trigger': 2,
#                             'cas': '75-05-08', 'ghs': 26},
#               {'description': 'Sodium Chloride', 'expiry_dur': 3, 'expiry_type': 'years', 'container_size': 500,
#                'container_units': 'g', 'requires_qual': False, 'reorder_qty': 2, 'reorder_trigger': 2,
#                'cas': '7647-14-5', 'ghs': 5},
#               {'description': 'Sodium Phosphate Dibsasic Heptahydrate', 'expiry_dur': 3, 'expiry_type': 'years',
#                'container_size': 500, 'container_units': 'g', 'requires_qual': False, 'reorder_qty': 2,
#                'reorder_trigger': 2, 'cas': '7782-85-6', 'ghs': 7},
#               {'description': 'Sodium Phosphate Monobasic Monohydrate', 'expiry_dur': 3, 'expiry_type': 'years',
#                'container_size': 500, 'container_units': 'g', 'requires_qual': False, 'reorder_qty': 2,
#                'reorder_trigger': 2, 'cas': '10049-21-5', 'ghs': 0},
#               {'description': 'Methanol, HPLC Grade', 'expiry_dur': 1, 'expiry_type': 'years', 'container_size': 4,
#                'container_units': 'L', 'requires_qual': False, 'reorder_qty': 4, 'reorder_trigger': 2, 'cas': '107018',
#                'ghs': 268},
#               {'description': 'Methanol, MS Grade', 'expiry_dur': 1, 'expiry_type': 'years', 'container_size': 1,
#                'container_units': 'L', 'requires_qual': False, 'reorder_qty': 6, 'reorder_trigger': 2, 'cas': '107018',
#                'ghs': 268}, {'description': 'DMEM', 'expiry_dur': 1, 'expiry_type': 'months', 'container_size': 1,
#                              'container_units': 'L', 'requires_qual': False, 'reorder_qty': 12, 'reorder_trigger': 4,
#                              'cas': 'NA', 'ghs': 7},
#               {'description': 'Decon-Ahol', 'expiry_dur': 1, 'expiry_type': 'months', 'container_size': 16,
#                'container_units': 'oz', 'requires_qual': False, 'reorder_qty': 48, 'reorder_trigger': 12,
#                'cas': '67-63-0', 'ghs': 27}]
# lots_seed = [{'template_id': 1.0, 'mfg_id': 1.0, 'lot_num': 'asdfkl3j', 'expiry': '03/07/2022'},
#              {'template_id': 1.0, 'mfg_id': 1.0, 'lot_num': 's723kaj', 'expiry': '11/23/2022'},
#              {'template_id': 1.0, 'mfg_id': 2.0, 'lot_num': 'dsl-23klj', 'expiry': '05/09/2021'},
#              {'template_id': 1.0, 'mfg_id': 2.0, 'lot_num': 'ldks2-23', 'expiry': '01/19/2021'},
#              {'template_id': 2.0, 'mfg_id': 1.0, 'lot_num': 'asdlg', 'expiry': '11/30/2021'},
#              {'template_id': 2.0, 'mfg_id': 1.0, 'lot_num': 'sdlkga-323', 'expiry': '12/15/2023'},
#              {'template_id': 2.0, 'mfg_id': 1.0, 'lot_num': 'sdlal3', 'expiry': '06/14/2024'},
#              {'template_id': 2.0, 'mfg_id': 1.0, 'lot_num': 'sdlkjag-3', 'expiry': '08/19/2023'},
#              {'template_id': 3.0, 'mfg_id': 3.0, 'lot_num': 'slka303', 'expiry': '10/12/2021'},
#              {'template_id': 3.0, 'mfg_id': 3.0, 'lot_num': 'asd01-33', 'expiry': '11/08/2020'},
#              {'template_id': 3.0, 'mfg_id': 3.0, 'lot_num': 'sdakag-3-32', 'expiry': '05/16/2021'},
#              {'template_id': 3.0, 'mfg_id': 3.0, 'lot_num': 'sdls-3jsdsg3', 'expiry': '07/16/2022'},
#              {'template_id': 4.0, 'mfg_id': 2.0, 'lot_num': 'sdlgas-3-ad', 'expiry': '08/02/2021'},
#              {'template_id': 4.0, 'mfg_id': 2.0, 'lot_num': 'alds-3', 'expiry': '07/09/2023'},
#              {'template_id': 4.0, 'mfg_id': 3.0, 'lot_num': 'dsj3a-3', 'expiry': '02/15/2021'},
#              {'template_id': 4.0, 'mfg_id': 3.0, 'lot_num': 'ajhga03y3', 'expiry': '09/16/2022'},
#              {'template_id': 5.0, 'mfg_id': 1.0, 'lot_num': 'sdkga-03hg', 'expiry': '06/08/2024'},
#              {'template_id': 5.0, 'mfg_id': 1.0, 'lot_num': 'hagd3ahg3', 'expiry': '12/19/2021'},
#              {'template_id': 5.0, 'mfg_id': 3.0, 'lot_num': 'dsjkgh033a', 'expiry': '11/30/2021'},
#              {'template_id': 5.0, 'mfg_id': 3.0, 'lot_num': 'dkhga3pd', 'expiry': '12/15/2023'},
#              {'template_id': 6.0, 'mfg_id': 2.0, 'lot_num': '3d-3-adhg', 'expiry': '06/14/2024'},
#              {'template_id': 6.0, 'mfg_id': 2.0, 'lot_num': 'ads-3iagn', 'expiry': '08/19/2023'},
#              {'template_id': 6.0, 'mfg_id': 2.0, 'lot_num': 'zla-3idjg', 'expiry': '10/12/2021'},
#              {'template_id': 6.0, 'mfg_id': 2.0, 'lot_num': 'zldei38hjg', 'expiry': '11/08/2020'},
#              {'template_id': 7.0, 'mfg_id': 2.0, 'lot_num': 'aldgz0zen', 'expiry': '05/16/2021'},
#              {'template_id': 7.0, 'mfg_id': 2.0, 'lot_num': 'dklaz-0id3', 'expiry': '07/16/2022'},
#              {'template_id': 7.0, 'mfg_id': 2.0, 'lot_num': 'dke3-k3', 'expiry': '08/02/2021'},
#              {'template_id': 7.0, 'mfg_id': 3.0, 'lot_num': 'qpeng-23', 'expiry': '07/09/2023'},
#              {'template_id': 8.0, 'mfg_id': 1.0, 'lot_num': 'dlnag73', 'expiry': '11/30/2021'},
#              {'template_id': 8.0, 'mfg_id': 1.0, 'lot_num': 'klg-03kjg', 'expiry': '12/15/2023'},
#              {'template_id': 8.0, 'mfg_id': 1.0, 'lot_num': 'apd83nng', 'expiry': '06/14/2024'},
#              {'template_id': 8.0, 'mfg_id': 1.0, 'lot_num': 'daog0-323', 'expiry': '08/19/2023'},
#              {'template_id': 9.0, 'mfg_id': 1.0, 'lot_num': 'adghe3', 'expiry': '10/12/2021'},
#              {'template_id': 9.0, 'mfg_id': 1.0, 'lot_num': 'adg93hgn', 'expiry': '11/08/2020'},
#              {'template_id': 9.0, 'mfg_id': 2.0, 'lot_num': 'dkangad-03', 'expiry': '05/16/2021'},
#              {'template_id': 9.0, 'mfg_id': 3.0, 'lot_num': 'dmangd-a3', 'expiry': '07/16/2022'}]
