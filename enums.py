from enum import Enum


class UnitsOfMeasure(Enum):
    LITERS = 11
    MILLILITERS = 12
    MICROLITERS = 13
    KILOGRAMS = 21
    GRAMS = 22
    MILLIGRAMS = 23
    MICROGRAMS = 24
    GALLONS = 31
    POUNDS = 32
    VIALS = 41
    KITS = 42
    OTHER = 51


class ExpiryTypes(Enum):
    NA = 1
    SINGLE = 2
    HOURS = 3
    DAYS = 4
    WEEKS = 5
    MONTHS = 6
    YEARS = 7


class ReagentStatus(Enum):
    UNOPENED = 1
    OPEN = 2
    QUARANTINE = 3
    DISCARDED = 4
