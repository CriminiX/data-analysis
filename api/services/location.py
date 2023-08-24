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
            util.replace_saint_names(util.remove_special_chars(city.lower())),
            util.remove_special_chars(neighborhood.lower()),
        )
        data_list_neighborhood = list(dict.fromkeys(data))
        return {"bairros": data_list_neighborhood}
    elif city is not None:
        data = get_city(
            util.replace_saint_names(util.remove_special_chars(city.lower()))
        )
        data_list_city = list(dict.fromkeys(data))
        return {"cidades": data_list_city}
    elif neighborhood is not None:
        data = get_neighborhood(util.remove_special_chars(neighborhood.lower()))
        data_list_neighborhood = list(dict.fromkeys(data))
        return {"bairros": data_list_neighborhood}
    elif zip_code is not None:
        locations = get_location_by_zip_code(zip_code)
        return LocationSearchResponse(
            records=[_to_location_response(loc) for loc in locations]
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
    neighborhood_df = table[table["bairro"].str.startswith(neighborhood, na=False)]
    if neighborhood_df.empty:
        raise LocationNotFound()
    return neighborhood_df["bairro"].values.tolist()


def get_city(city: str):
    table = get_table("locations")
    city_df = table[table["cidade"].str.startswith(city, na=False)]
    if city_df.empty:
        raise LocationNotFound()
    return city_df["cidade"].values.tolist()


def get_neighborhood_by_city(city: str, neighborhood: str) -> list[str]:
    table = get_table("locations")
    neighborhood_df = table[
        table["cidade"].str.startswith(city, na=False)
        & table["bairro"].str.startswith(neighborhood, na=False)
    ]
    if neighborhood_df.empty:
        raise LocationNotFound()
    return neighborhood_df["bairro"].values.tolist()

def get_location_by_zip_code(zip_code: str):
    table = get_table("locations")
    locations = table[table["cep"].str.startswith(zip_code, na=False)]
    if locations.empty:
        raise LocationNotFound()
    return locations[["cidade", "bairro", "cep"]].sort_values(["cidade", "bairro"]).to_dict(orient="records")

def _to_location_response(location_data: dict):
    neighborhood = location_data.get("bairro")
    city = location_data.get("cidade")
    zip_code = location_data.get("cep")
    return LocationRef(city=city, neighborhood=neighborhood, zip_code=zip_code)
