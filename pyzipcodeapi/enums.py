from enum import Enum


class FormatEnum(str, Enum):
    JSON = "json"
    XML = "xml"
    CSV = "csv"


class UnitEnum(str, Enum):
    KM = "km"
    MILE = "mile"


class CountryEnum(str, Enum):
    US = "US"
    CA = "CA"
