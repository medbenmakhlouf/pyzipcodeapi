# -*- coding: utf-8 -*-
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import csv
import requests

from pyzipcodeapi.options import OPTIONS

BASE_URL = 'https://www.zipcodeapi.com/rest/{api_key}/{option}.{format}/'
FORMAT = ['json', 'xml', 'csv']


class ZipCodeApiRequest(object):
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
            if kwargs['units'] not in self.option['units']:
                raise ValueError(
                    "%s unit is not available. ZipCodeApi's units for the option '%s' should be in %s" %
                    (str(kwargs['units']), str(self.option['name']), str(', '.join(self.option['units'])))
                )
        except KeyError:
            pass
        url = self.base_url + self.option['url'].format(**kwargs)
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
        if self.output_format == 'json':
            return request.json()
        elif self.output_format == 'csv':
            f = StringIO(request.text)
            reader = csv.DictReader(f, delimiter=',')
            return reader
        return request.text


class ZipCodeApi(object):
    def __init__(self, api_key):
        """
        :param api_key: 
        """
        self.api_key = api_key

    def get(self, option, output_format='json'):
        """
        :param option: 
        :param output_format: 
        :return: 
        """
        if option not in OPTIONS:
            raise KeyError(
                'Option {0} is not valid'.format(option) +
                "ZipCodeApi's option should be in %s" % str(', '.join(OPTIONS.keys()))
            )
        if output_format not in FORMAT:
            raise ValueError(
                "%s format is not available. ZipCodeApi's format should be in %s" %
                (str(output_format), str(', '.join(FORMAT)))
            )
        base_url = BASE_URL.format(api_key=self.api_key, option=option, format=output_format)
        return ZipCodeApiRequest(base_url, OPTIONS[option], output_format)
