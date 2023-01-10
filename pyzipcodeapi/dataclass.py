from dataclasses import dataclass


@dataclass
class Error:
    error_code: int
    error_msg: str


@dataclass
class Distance:
    distance: float


@dataclass
class MultiDistance:
    distances: dict[str, float]


@dataclass
class RadiusInfo:
    zip_code: str
    distance: float
    city: str
    state: str


@dataclass
class Radius:
    zip_codes: list[str | dict]

    @property
    def info(self) -> list[RadiusInfo | str]:
        if self.zip_codes and type(self.zip_codes[0] == dict):
            return [RadiusInfo(**zp) for zp in self.zip_codes]
        return self.zip_codes


@dataclass
class MultiRadiusInfo:
    base_zip_code: str
    zip_codes: list[str]


@dataclass
class MultiRadius:
    responses: list[dict]

    @property
    def info(self) -> list[MultiRadiusInfo]:
        return [MultiRadiusInfo(**r) for r in self.responses]


@dataclass
class MatchClose:
    zip_code1: str
    zip_code2: str
    distance: float


@dataclass
class Info:
    zip_code: str
    lat: float
    lng: float
    city: str
    state: str
    timezone: dict
    acceptable_city_names: list[dict]
    area_codes: list[int]


@dataclass
class ZipCode:
    zip_codes: list[str]
