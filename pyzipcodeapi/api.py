from csv import DictReader
from http.client import HTTPSConnection
from io import StringIO
from json import loads
from urllib.parse import quote_plus, urlencode
from xml.etree.ElementTree import Element, fromstring

from pyzipcodeapi.dataclass import (
    Distance,
    Error,
    Info,
    MatchClose,
    MultiDistance,
    MultiRadius,
    Radius,
    ZipCode,
)
from pyzipcodeapi.enums import CountryEnum, DistanceUnitEnum, FormatEnum, GeoUnitEnum

ResultType = DictReader | bytes | type | Element | Error | list[type]


class ZipCodeApi:
    host: str = "www.zipcodeapi.com"

    def __init__(
        self,
        api_key: str,
        f: FormatEnum = FormatEnum.JSON,
        country: CountryEnum = CountryEnum.US,
    ):
        self.api_key = api_key
        self.format = f
        self.country = country
        self.con = HTTPSConnection(host=self.host)

    def _api_call(
        self,
        method: str,
        option: str,
        path: str,
        body: str | None = None,
        headers: dict | None = None,
    ):
        base_url = "rest/v2/CA" if self.country == CountryEnum.CA else "rest"
        self.con.request(
            method=method,
            url=f"/{base_url}/{self.api_key}/{option}.{self.format}/{path}",
            body=body,
            headers={} if headers is None else headers,
        )

    def _get(self, option: str, path: str):
        self._api_call(method="GET", option=option, path=path)

    def _post(self, option: str, path: str, data: dict):
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        self._api_call(
            method="POST",
            option=option,
            path=path,
            body=urlencode(data),
            headers=headers,
        )

    def _parse_response(self, data_class: type | None = None) -> ResultType:
        response = self.con.getresponse()
        success = response.status == 200
        data = response.read()
        if self.format == FormatEnum.JSON:
            data = loads(data)
            if success:
                if data_class:
                    if type(data) == dict:
                        return data_class(**data)
                    if type(data) == list:
                        return [data_class(**d) for d in data]
                return data
            return Error(**data)
        elif self.format == FormatEnum.CSV:
            return DictReader(StringIO(data.decode()), delimiter=",")
        elif self.format == FormatEnum.XML:
            if success:
                return fromstring(data.decode())
        return data

    def distance(
        self,
        zip_code1: str,
        zip_code2: str,
        units: DistanceUnitEnum = DistanceUnitEnum.KM,
    ) -> Distance | DictReader | Element:
        """distance.<format>/<zip_code1>/<zip_code2>/<units>"""
        self._get("distance", f"{zip_code1}/{zip_code2}/{units}")
        return self._parse_response(data_class=Distance)

    def multi_distance(
        self,
        zip_code: str,
        zip_codes: list[str],
        units: DistanceUnitEnum = DistanceUnitEnum.KM,
    ) -> MultiDistance | DictReader | Element:
        """multi-distance.<format>/<zip_code>/<other_zip_codes>/<units>"""
        assert len(zip_codes) <= 100
        self._get("multi-distance", f"{zip_code}/{','.join(zip_codes)}/{units}")
        return self._parse_response(data_class=MultiDistance)

    def radius(
        self,
        zip_code: str,
        distance: float,
        minimal: bool = False,
        units: DistanceUnitEnum = DistanceUnitEnum.KM,
    ) -> Radius | DictReader | Element:
        """radius.<format>/<zip_code>/<distance>/<units>"""
        path = f"{zip_code}/{distance}/{units}"
        if minimal:
            path = f"{path}?minimal"
        self._get("radius", path)
        return self._parse_response(data_class=Radius)

    def multi_radius(
        self,
        distance: float,
        zip_codes: list[str] | None = None,
        addresses: list[str] | None = None,
        units: DistanceUnitEnum = DistanceUnitEnum.KM,
    ) -> MultiRadius | DictReader | Element:
        """multi-radius.<format>/<distance>/<units>"""
        if zip_codes is None and addresses is None:
            raise ValueError
        body = dict()
        if zip_codes:
            assert len(zip_codes) <= 100
            body["zip_codes"] = "\n".join(zip_codes)
        if addresses:
            assert len(addresses) <= 100
            body["addrs"] = "\n".join(addresses)
        self._post("multi-radius", f"{distance}/{units}", data=body)
        return self._parse_response(data_class=MultiRadius)

    def match_close(
        self,
        zip_codes: list[str],
        distance: float,
        units: DistanceUnitEnum = DistanceUnitEnum.KM,
    ) -> list[MatchClose] | DictReader | Element:
        """match-close.<format>/<zip_codes>/<distance>/<units>"""
        self._get("match-close", f"{','.join(zip_codes)}/{distance}/{units}")
        return self._parse_response(data_class=MatchClose)

    def info(
        self, zip_code: str, units: GeoUnitEnum = GeoUnitEnum.DEGREES
    ) -> Info | DictReader | Element:
        """info.<format>/<zip_code>/<units>"""
        self._get("info", f"{zip_code}/{units}")
        return self._parse_response(data_class=Info)

    def multi_info(
        self, zip_codes: list[str], units: GeoUnitEnum = GeoUnitEnum.DEGREES
    ) -> dict[str, dict] | DictReader | Element:
        """multi-info.<format>/<zip_code>/<units>"""
        self._get("multi-info", f"{','.join(zip_codes)}/{units}")
        return self._parse_response()

    def city_zip_codes(self, city: str, state: str) -> ZipCode | DictReader | Element:
        """
        US: city-zips.<format>/<city>/<state>
        CA: city-postal-codes.<format>/<city>/<province>
        """
        option = "city-postal-codes" if self.country == CountryEnum.CA else "city-zips"
        self._get(option, f"{quote_plus(city)}/{quote_plus(state)}")
        return self._parse_response(data_class=ZipCode)

    def state_zip_codes(self, state: str) -> ZipCode | DictReader | Element:
        """state-zips.<format>/<state>"""
        self._get("state-zips", quote_plus(state))
        return self._parse_response(data_class=ZipCode)

    def radius_sql(
        self,
        lat: float,
        long: float,
        distance: float,
        lat_long_units: GeoUnitEnum = GeoUnitEnum.DEGREES,
        units: DistanceUnitEnum = DistanceUnitEnum.KM,
        lat_field_name: str = "lat",
        long_field_name: str = "long",
        precision: int = 1,
    ) -> Radius | DictReader | Element:
        """radius-sql.<format>/<lat>/<long>/<lat_long_units>/<distance>/<units>/<lat_field_name>/
        <long_field_name>/<precision>"""
        assert precision <= 16
        args = [
            str(lat),
            str(long),
            lat_long_units,
            str(distance),
            units,
            lat_field_name,
            long_field_name,
            str(precision),
        ]
        self._get("radius-sql", "/".join(args))
        return self._parse_response()
