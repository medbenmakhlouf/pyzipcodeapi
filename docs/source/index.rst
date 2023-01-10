Welcome to Py Zip Code API's documentation!
===========================================
Py ZipCodeApi will make it easier for you to use the different options in `ZipCodeAPI`_.

.. _ZipCodeAPI: https://www.zipcodeapi.com/API


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
    * `multi-distance`_
    * `radius`_
    * `multi-radius`_
    * `match-close`_
    * `info`_
    * `multi-info`_
    * `city-zips`_
    * `state-zips`_
    * `radius-sql`_

.. _distance: https://www.zipcodeapi.com/API#distance
.. _multi-distance: https://www.zipcodeapi.com/API#multiZipDistance
.. _radius: https://www.zipcodeapi.com/API#radius
.. _multi-radius: https://www.zipcodeapi.com/API#multi-radius
.. _match-close: https://www.zipcodeapi.com/API#matchClose
.. _info: https://www.zipcodeapi.com/API#zipToLoc
.. _multi-info: https://www.zipcodeapi.com/API#multiZipToLoc
.. _city-zips: https://www.zipcodeapi.com/API#locToZips
.. _state-zips: https://www.zipcodeapi.com/API#stateToZips
.. _radius-sql: https://www.zipcodeapi.com/API#radiusSql

Example
=======

.. code-block:: python

    # set different inputs
    f2 = FormatEnum.JSON
    ud = DistanceUnitEnum.KM
    ug = GeoUnitEnum.DEGREES
    us = CountryEnum.US
    ca = CountryEnum.CA
    zca = ZipCodeApi(api_key=API_KEY, f=f2, country=us)
    # https://www.zipcodeapi.com/rest/<api_key>/distance.<format>/<zip_code1>/<zip_code2>/<units>
    print(zca.distance(zip_code1="94106", zip_code2="94132", units=ud))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/multi-distance.<format>/<zip_code>/<other_zip_codes>/<units>
    print(zca.multi_distance(zip_code="94106", zip_codes=["94132"], units=ud))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/radius.<format>/<zip_code>/<distance>/<units>
    print(zca.radius(zip_code="94120", distance=5, units=ud, minimal=False))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/multi-radius.<format>/<zip_code>/<distance>/<units>
    print(
        zca.multi_radius(
            distance=5,
            zip_codes=["22911", "22902"],
            addresses=["1827 Glissade Ln, Charlottesville VA 22911"],
            units=ud,
        )
    )
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/match-close.<format>/<zip_codes>/<distance>/<units>
    print(zca.match_close(zip_codes=["22911", "22902"], distance=120, units=ud))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/info.<format>/<zip_code>/<units>
    print(zca.info(zip_code="22911", units=ug))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/multi-info.<format>/<zip_code>/<units>
    print(zca.multi_info(zip_codes=["22911"], units=ug))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/city-zips.<format>/<city>/<state>
    print(zca.city_zip_codes(city="New York", state="VA"))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/state-zips.<format>/<state>
    print(zca.state_zip_codes(state="VA"))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/radius-sql.<format>/<lat>/<long>/<lat_long_units>/<distance>/<units>/
    # <lat_field_name>/<long_field_name>/<precision>
    print(
        zca.radius_sql(
            lat=37.722223,
            long=-122.484048,
            lat_long_units=ug,
            distance=5,
            units=ud,
            lat_field_name="lat",
            long_field_name="long",
            precision=4,
        )
    )

Output
======

for each request you make, you can choose between the different outputs :

    * json
    * csv (the output is an instance from CSV Reader Objects `DictReader`_)
    * xml


.. warning:: Depend on the option you will choose, Please refer to the `original website`_ to see the context of each output.


.. _DictReader: https://docs.python.org/3/library/csv.html#csv.DictReader
.. _original website: https://www.zipcodeapi.com/API

Contributing
============

To contribute to PyZipCodeAPI `create a fork`_ on GitHub. Clone your fork, make some changes, and submit a pull request.

.. _create a fork: https://github.com/medbenmakhlouf/pyzipcodeapi

Issues
======

Use the GitHub `issue tracker`_ for PyZipCodeAPI to submit bugs, issues, and feature requests.

.. _issue tracker: https://github.com/medbenmakhlouf/pyzipcodeapi/issues

