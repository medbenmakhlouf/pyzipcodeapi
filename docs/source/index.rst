Welcome to Py Zip Code API's documentation!
===========================================
Py ZipCodeApi will make it easier for you to use the different options in `ZipCodeAPI`_.

.. _ZipCodeAPI: https://www.zipcodeapi.com/API

.. toctree::
   :maxdepth: 1
    :glob:

Installation
============

Use pip to install from PyPI::

    pip install pyzipcodeapi

Register for free ``api_key`` `here`_.

.. _here: https://www.zipcodeapi.com/Register

Options
=======

As mentioned in the original website. the following options are supported in this package :

    * `distance`_
    * `radius`_
    * `match-close`_
    * `info`_
    * `multi-info`_
    * `city-zips`_
    * `radius-sql`_

.. _distance: https://www.zipcodeapi.com/API#distance
.. _radius: https://www.zipcodeapi.com/API#radius
.. _match-close: https://www.zipcodeapi.com/API#matchClose
.. _info: https://www.zipcodeapi.com/API#zipToLoc
.. _multi-info: https://www.zipcodeapi.com/API#multiZipToLoc
.. _city-zips: https://www.zipcodeapi.com/API#locToZips
.. _radius-sql: https://www.zipcodeapi.com/API#radiusSql

Example
=======

.. code-block:: python

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



Contributing
============

To contribute to Py ZipCodeAPI `create a fork`_ on GitHub. Clone your fork, make some changes, and submit a pull request.

.. _create a fork: https://github.com/medbenmakhlouf/pyzipcodeapi

Issues
======

Use the GitHub `issue tracker`_ for django-storages to submit bugs, issues, and feature requests.

.. _issue tracker: https://github.com/medbenmakhlouf/pyzipcodeapi/issues

