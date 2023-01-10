from enum import Enum


class FormatEnum(str, Enum):
    JSON = "json"
    XML = "xml"
    CSV = "csv"


class DistanceUnitEnum(str, Enum):
    KM = "km"
    MILE = "mile"


class GeoUnitEnum(str, Enum):
    DEGREES = "degrees"
    RADIANS = "radians"


class CountryEnum(str, Enum):
    US = "US"
    CA = "CA"
