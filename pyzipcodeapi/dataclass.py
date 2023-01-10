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
