# -*- coding: utf-8 -*-
from pyzipcodeapi.api import ZipCodeApi

API_KEY = '3dAoRheoltlrRLipalNn8LkhJAh59P5c2GAUXOjjhEK9p2zAomYw7iORS5X1U2eX'

if __name__ == '__main__':
    # set different inputs
    f = 'json'
    u = 'km'
    ou = 'degrees'
    obj = ZipCodeApi(API_KEY)
    #  https://www.zipcodeapi.com/rest/<api_key>/distance.<format>/<zip_code1>/<zip_code2>/<units>
    print(obj.get('distance', f).filter(zip_code1='94106', zip_code2='94132', units=u))
    print('------------------')
    # https://www.zipcodeapi.com/rest/<api_key>/radius.<format>/<zip_code>/<distance>/<units>
    print(obj.get('radius', f).filter(zip_code='94120', distance='94132', units=u))
    print('------------------')
    # https://www.zipcodeapi.com/rest/<api_key>/match-close.<format>/<zip_codes>/<distance>/<units>
    print(obj.get('match-close', f).filter(zip_codes='941asd32', distance='5', units=u))
    print('------------------')
    # https://www.zipcodeapi.com/rest/<api_key>/info.<format>/<zip_code>/<units>
    print(obj.get('info', f).filter(zip_code='94132', units=ou))
    print('------------------')
    # https://www.zipcodeapi.com/rest/<api_key>/multi-info.<format>/<zip_code>/<units>
    print(obj.get('multi-info', f).filter(zip_code='94132', units=ou))
    print('------------------')
    # https://www.zipcodeapi.com/rest/<api_key>/city-zips.<format>/<city>/<state>
    print(obj.get('city-zips', f).filter(city='San Francisco', state='CA'))
    print('------------------')
    # https://www.zipcodeapi.com/rest/<api_key>/radius-sql.<format>/<lat>/<long>/<lat_long_units>/<distance>/<units>/
    # <lat_field_name>/<long_field_name>/<precision>
    print(obj.get('radius-sql', f).filter(
        lat='37.722223',
        long='-122.484048',
        lat_long_units=ou,
        distance='5',
        units=u,
        lat_field_name='lat',
        long_field_name='long',
        precision='4'
    ))
