from csv import DictReader
from http.client import HTTPSConnection
from io import StringIO
from json import loads
from xml.etree.ElementTree import Element, fromstring

import requests

from pyzipcodeapi.dataclass import Distance, Error
from pyzipcodeapi.enums import FormatEnum, UnitEnum, CountryEnum
from pyzipcodeapi.options import OPTIONS

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

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.con = HTTPSConnection(host=self.host)

    def _make_api_call(
        self,
        option: str,
        f: FormatEnum,
        path: str,
        country: CountryEnum = CountryEnum.US,
        data_class: type | None = None,
    ) -> DictReader | bytes | type | Element | Error:
        base_url = f"rest/v2/CA" if country == CountryEnum.CA else f"rest"
        self.con.request(
            method="GET", url=f"/{base_url}/{self.api_key}/{option}.{f}/{path}"
        )
        response = self.con.getresponse()
        success = response.status == 200
        data = response.read()
        if f == FormatEnum.JSON:
            data = loads(data)
            if success:
                return data_class(**data) if data_class else data
            return Error(**data)
        elif f == FormatEnum.CSV:
            return DictReader(StringIO(data.decode()), delimiter=",")
        elif f == FormatEnum.XML:
            if success:
                return fromstring(data.decode())
        return data

    def distance(
        self,
        zip_code1: str,
        zip_code2: str,
        units: UnitEnum = UnitEnum.KM,
        f: FormatEnum | None = FormatEnum.JSON,
        country: CountryEnum = CountryEnum.US,
    ) -> Distance | DictReader | Element:
        """distance.<format>/<zip_code1>/<zip_code2>/<units>"""
        return self._make_api_call(
            "distance",
            f,
            path=f"{zip_code1}/{zip_code2}/{units}",
            country=country,
            data_class=Distance,
        )
