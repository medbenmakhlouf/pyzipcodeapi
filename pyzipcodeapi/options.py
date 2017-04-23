# -*- coding: utf-8 -*-
"""
https://www.zipcodeapi.com/rest/<api_key>/distance.<format>/<zip_code1>/<zip_code2>/<units>
https://www.zipcodeapi.com/rest/<api_key>/radius.<format>/<zip_code>/<distance>/<units>
https://www.zipcodeapi.com/rest/<api_key>/match-close.<format>/<zip_codes>/<distance>/<units>
https://www.zipcodeapi.com/rest/<api_key>/info.<format>/<zip_code>/<units>
https://www.zipcodeapi.com/rest/<api_key>/multi-info.<format>/<zip_code>/<units>.
https://www.zipcodeapi.com/rest/<api_key>/city-zips.<format>/<city>/<state>.
https://www.zipcodeapi.com/rest/<api_key>/radius-sql.<format>/<lat>/<long>/<lat_long_units>/<distance>/<units>/<lat_field_name>/<long_field_name>/<precision>. 
"""
OPTIONS = {
    'distance': {
        'name': 'API Zip Code Distance',
        'url': '{zip_code1}/{zip_code2}/{units}',
        'units': ['km', 'mile']
    },
    'radius': {
        'name': 'API Zip Codes by Radius',
        'url': '{zip_code}/{distance}/{units}',
        'units': ['km', 'mile']
    },
    'match-close': {
        'name': 'API Find Close Zip Codes',
        'url': '{zip_codes}/{distance}/{units}',
        'units': ['km', 'mile']
    },
    'info': {
        'name': 'API Zip Code to Location Information',
        'url': '{zip_code}/{units}',
        'units': ['degrees', 'radians']
    },
    'multi-info': {
        'name': 'API Multiple Zip Codes to Location Information',
        'url': '{zip_code}/{units}',
        'units': ['degrees', 'radians']
    },
    'city-zips': {
        'name': 'API Location to Zip Codes',
        'url': '{city}/{state}',
    },
    'radius-sql': {
        'name': 'API/SQL Latitude/Longitude SQL WHERE Clause for Radius',
        'url': '{lat}/{long}/{lat_long_units}/{distance}/{units}/{lat_field_name}/{long_field_name}/{precision}',
        'units': ['km', 'mile']
    }
}
