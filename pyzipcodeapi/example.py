from pyzipcodeapi.api import ZipCodeApi, ZipCodeApiV2
from pyzipcodeapi.enums import FormatEnum, UnitEnum, CountryEnum

API_KEY = "DemoOnly00yDUhTAzyzlwpXrk6SuiuvD80IAvhCJowPjA5Cqgz9vb7QyIyzDE77r"

if __name__ == "__main__":
    # set different inputs
    f = "json"
    u = "km"
    ou = "degrees"
    obj = ZipCodeApi(API_KEY)
    # V2
    zca = ZipCodeApiV2(api_key=API_KEY)
    f2 = FormatEnum.JSON
    u2 = UnitEnum.KM
    us = CountryEnum.US
    ca = CountryEnum.CA
    # https://www.zipcodeapi.com/rest/<api_key>/distance.<format>/<zip_code1>/<zip_code2>/<units>
    print(
        zca.distance(zip_code1="94106", zip_code2="94132", units=u2, f=f2, country=us)
    )
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/multi-distance.<format>/<zip_code>/<other_zip_codes>/<units>
    print(zca.multi_distance(zip_code="94106", zip_codes=["94132"], units=u2, f=f2))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/radius.<format>/<zip_code>/<distance>/<units>
    print(zca.radius(zip_code="94120", distance=5, units=u2, minimal=False))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/multi-radius.<format>/<zip_code>/<distance>/<units>
    print(
        zca.multi_radius(
            distance=5,
            zip_codes=["22911", "22902"],
            addresses=["1827 Glissade Ln, Charlottesville VA 22911"],
            units=u2,
        )
    )
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/match-close.<format>/<zip_codes>/<distance>/<units>
    print(obj.get("match-close", f).filter(zip_codes="941asd32", distance="5", units=u))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/info.<format>/<zip_code>/<units>
    print(obj.get("info", f).filter(zip_code="94132", units=ou))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/multi-info.<format>/<zip_code>/<units>
    print(obj.get("multi-info", f).filter(zip_code="94132", units=ou))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/city-zips.<format>/<city>/<state>
    print(obj.get("city-zips", f).filter(city="San Francisco", state="CA"))
    print("------------------")
    # https://www.zipcodeapi.com/rest/<api_key>/radius-sql.<format>/<lat>/<long>/<lat_long_units>/<distance>/<units>/
    # <lat_field_name>/<long_field_name>/<precision>
    print(
        obj.get("radius-sql", f).filter(
            lat="37.722223",
            long="-122.484048",
            lat_long_units=ou,
            distance="5",
            units=u,
            lat_field_name="lat",
            long_field_name="long",
            precision="4",
        )
    )
