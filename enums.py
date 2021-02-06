from enum import Enum


class UnitsOfMeasure(Enum):
    L = 'liters'
    ML = 'milliliters'
    UL = 'microliters'
    KG = 'kilograms'
    G = 'grams'
    MG = 'milligrams'
    UG = 'micrograms'
    GA = 'gallons'
    LB = 'pounds'
    V = 'vials'
    K = 'kits'


class ExpiryTypes(Enum):
    N = 'NA'
    S = 'single'
    H = 'hours'
    D = 'days'
    W = 'weeks'
    M = 'months'
    Y = 'years'


class ReagentStatus(Enum):
    U = 'unopened'
    O = 'open'
    Q = 'quarantine'
    D = 'discarded'
