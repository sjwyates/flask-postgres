import enum
import json


class ReagentStatus(enum.Enum):
    # create type reagent_status as enum ('Unopened', 'Open', 'Quarantine', 'Discarded');
    Unopened = "Unopened"
    Open = "Open"
    Quarantine = "Quarantine"
    Discarded = "Discarded"

    def __str__(self):
        return str(self.value)


class ExpiryTypes(enum.Enum):
    # create type expirytypes as enum ('single_use', 'hours', 'days', 'weeks', 'months', 'years');
    single_use = "single_use"
    hours = "hours"
    days = "days"
    weeks = "weeks"
    months = "months"
    years = "years"

    def __str__(self):
        return str(self.value)


class ContainerUnits(enum.Enum):
    # create type containerunits as enum ('L', 'mL', 'uL', 'kg', 'g', 'mg', 'ug', 'ga', 'oz', 'vials', 'kits', 'units');
    L = "L"
    mL = "mL"
    uL = "uL"
    kg = "kg"
    g = "g"
    mg = "mg"
    ug = "ug"
    ga = "ga"
    oz = "oz"
    vials = "vials"
    kits = "kits"
    units = "units"

    def __str__(self):
        return str(self.value)


PUBLIC_ENUMS = {
    'ReagentStatus': ReagentStatus,
    'ExpiryTypes': ExpiryTypes,
    'ContainerUnits': ContainerUnits
}


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in PUBLIC_ENUMS.values():
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d
