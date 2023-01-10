from dataclasses import dataclass


@dataclass
class Error:
    error_code: int
    error_msg: str


@dataclass
class Distance:
    distance: float
