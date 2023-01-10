from csv import DictReader
from http.client import HTTPSConnection
from io import StringIO
from json import loads
from urllib.parse import quote_plus, urlencode
from xml.etree.ElementTree import Element, fromstring

import requests

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
from pyzipcodeapi.options import OPTIONS

ResultType = DictReader | bytes | type | Element | Error | list[type]

BASE_URL = "https://www.zipcodeapi.com/rest/{api_key}/{option}.{format}/"
FORMAT = ["json", "xml", "csv"]


class ZipCodeApiRequest:
    def __init__(self, base_url, option, output_format):
        """
        :param base_url:
        :param option:
        :param output_format:
        """
        self.base_url = base_url
        self.option = option
        self.output_format = output_format
        self.requests = requests

    def filter(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        try:
            if kwargs["units"] not in self.option["units"]:
                raise ValueError(
                    "%s unit is not available. ZipCodeApi's units for the option '%s' should be in %s"
                    % (
                        str(kwargs["units"]),
                        str(self.option["name"]),
                        str(", ".join(self.option["units"])),
                    )
                )
        except KeyError:
            pass
        url = self.base_url + self.option["url"].format(**kwargs)
        return self.make_request(url)

    def make_request(self, url):
        """
        :param url:
        :return:
        """
        r = self.requests.get(url)
        return self.request_output(r)

    def request_output(self, request):
        """
        :param request:
        :return:
        """
        if self.output_format == "json":
            return request.json()
        elif self.output_format == "csv":
            f = StringIO(request.text)
            reader = DictReader(f, delimiter=",")
            return reader
        return request.text


class ZipCodeApi:
    def __init__(self, api_key):
        """
        :param api_key:
        """
        self.api_key = api_key

    def get(self, option, output_format="json"):
        """
        :param option:
        :param output_format:
        :return:
        """
        if option not in OPTIONS:
            raise KeyError(
                f"Option {option} is not valid"
                + "ZipCodeApi's option should be in %s" % str(", ".join(OPTIONS.keys()))
            )
        if output_format not in FORMAT:
            raise ValueError(
                "%s format is not available. ZipCodeApi's format should be in %s"
                % (str(output_format), str(", ".join(FORMAT)))
            )
        base_url = BASE_URL.format(
            api_key=self.api_key, option=option, format=output_format
        )
        return ZipCodeApiRequest(base_url, OPTIONS[option], output_format)


class ZipCodeApiV2:
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
        distance: int,
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
        distance: int,
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
        distance: int,
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

    def city_zip_codes(
        self, city: str, state: str
    ) -> ZipCode | DictReader | Element:
        """
        US: city-zips.<format>/<city>/<state>
        CA: city-postal-codes.<format>/<city>/<province>
        """
        option = "city-postal-codes" if self.country == CountryEnum.CA else "city-zips"
        self._get(option, f"{quote_plus(city)}/{quote_plus(state)}")
        return self._parse_response(data_class=ZipCode)

    def state_zip_codes(self, state: str) -> ZipCode | DictReader | Element:
        """state-zips.<format>/<state>"""
        self._get("state-zips", f"{quote_plus(state)}")
        return self._parse_response(data_class=ZipCode)
