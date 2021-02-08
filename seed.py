from enums import UnitsOfMeasure, ExpiryTypes, ReagentStatus
from datetime import datetime

manufacturers = [
    'Fisher',
    'Sigma',
    'VWR'
]

reagent_templates = [
    {
        'description': 'Acetic Acid',
        'expiry_dur': 1,
        'expiry_type': 'Years',
        'container_size': 500,
        'container_units': 'Milliliters',
        'requires_qual': False
    },
    {
        'description': 'Acetone',
        'expiry_dur': 1,
        'expiry_type': 'Years',
        'container_size': 1,
        'container_units': 'Liters',
        'requires_qual': False
    },
    {
        'description': 'Acetonitrile',
        'expiry_dur': 1,
        'expiry_type': 'Years',
        'container_size': 4,
        'container_units': 'Liters',
        'requires_qual': False
    }
]

lots = [
    {
        'temp_id': 1,
        'mfg_id': 1,
        'lot_num': 'abc123',
        'expiry': datetime(2022, 11, 4, 0, 0),
    },
    {
        'temp_id': 1,
        'mfg_id': 1,
        'lot_num': 'def456',
        'expiry': datetime(2023, 8, 19, 0, 0),
    },
    {
        'temp_id': 1,
        'mfg_id': 2,
        'lot_num': '123abc',
        'expiry': datetime(2021, 6, 12, 0, 0),
    }
]

reagents = [
    {
        'template_id': 1,
        'lot_id': 1,
        'expiry': datetime(2022, 11, 4, 0, 0),
        'status': 'Unopened'
    }
]