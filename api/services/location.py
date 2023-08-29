from exceptions import MissingRequiredValues
from store.data_store import get_table
import util
from schemas.shared import Location
from schemas.responses import LocationRef, LocationSearchResponse



class LocationNotFound(Exception):
    pass


def search(city: str | None, neighborhood: str | None, zip_code: str | None):
    if city is not None and neighborhood is not None:
        data = get_neighborhood_by_city(
            util.remove_special_chars(city.lower()),
            util.remove_special_chars(neighborhood.lower()),
        )
        return LocationSearchResponse(records=[_to_location_ref(record) for record in data])
    elif city is not None:
        data = get_city(
            util.remove_special_chars(city.lower())
        )
        return LocationSearchResponse(records=[LocationRef(city=record) for record in data])
    elif neighborhood is not None:
        data = get_neighborhood(util.remove_special_chars(neighborhood.lower()))
        return LocationSearchResponse(records=[LocationRef(neighborhood=record) for record in data])
    elif zip_code is not None:
        locations = get_location_by_zip_code(zip_code)
        return LocationSearchResponse(
            records=[_to_location_ref(loc) for loc in locations]
        )
    else:
        raise MissingRequiredValues(["city", "neighborhood", "zip_code"])


def get_code_by_location(loc: Location) -> int | None:
    table = get_table("locations")
    neighborhood = table[
        (table["cidade"] == loc.city) & (table["bairro"] == loc.neighborhood)
    ]
    if neighborhood.empty:
        raise LocationNotFound()

    return neighborhood["neighborhood_code"].iat[0]


def get_neighborhood(neighborhood: str):
    table = get_table("locations")
    neighborhood_df = table[table["bairro"].str.contains(neighborhood, na=False, regex=False)]
    if neighborhood_df.empty:
        raise LocationNotFound()
    return neighborhood_df["bairro"].drop_duplicates().values.tolist()


def get_city(city: str):
    table = get_table("locations")
    city_df = table[table["cidade"].str.contains(city, na=False, regex=False)]
    if city_df.empty:
        raise LocationNotFound()
    return city_df["cidade"].drop_duplicates().values.tolist()


def get_neighborhood_by_city(city: str, neighborhood: str) -> list[str]:
    table = get_table("locations")
    neighborhood_df = table[
        table["cidade"].str.contains(city, na=False, regex=False)
        & table["bairro"].str.contains(neighborhood, na=False, regex=False)
    ]
    if neighborhood_df.empty:
        raise LocationNotFound()
    return neighborhood_df[["cidade", "bairro"]].drop_duplicates().sort_values(["cidade", "bairro"]).to_dict(orient="records")

def get_location_by_zip_code(zip_code: str):
    zip_codes = get_table("zip_codes")
    locations = get_table("locations")
    location_code = zip_codes[zip_codes["cep"] == zip_code]
    if location_code.empty:
        raise LocationNotFound()
    code: str = location_code["neighborhood_code"].iat[0]
    result = locations[locations["neighborhood_code"] == code]
    if result.empty:
        raise LocationNotFound()
    return result[["cidade", "bairro"]].assign(cep=zip_code).drop_duplicates(subset=["cidade", "bairro"]).sort_values(["cidade", "bairro"]).to_dict(orient="records")

def _to_location_ref(location_data: dict):
    neighborhood = location_data.get("bairro")
    city = location_data.get("cidade")
    zip_code = location_data.get("cep")
    return LocationRef(city=city, neighborhood=neighborhood, zip_code=zip_code)
