from pyzipcodeapi.api import ZipCodeApi
from pyzipcodeapi.enums import CountryEnum, DistanceUnitEnum, FormatEnum, GeoUnitEnum

API_KEY = "DemoOnly00yDUhTAzyzlwpXrk6SuiuvD80IAvhCJowPjA5Cqgz9vb7QyIyzDE77r"

if __name__ == "__main__":
    # set different inputs
    # V2
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
