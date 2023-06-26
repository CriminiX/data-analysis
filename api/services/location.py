from store.data_store import get_table
import util
from schemas.shared import Location


class LocationNotFound(Exception):
    pass


def search(city: str, neighborhood: str):
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
    neighborhood = table[table["bairro"].str.contains(neighborhood, regex=False)]
    if neighborhood.empty:
        raise LocationNotFound()
    return neighborhood["bairro"].values.tolist()


def get_city(city: str):
    table = get_table("locations")
    city = table[table["cidade"].str.contains(city, regex=False)]
    if city.empty:
        raise LocationNotFound()
    return city["cidade"].values.tolist()


def get_neighborhood_by_city(city: str, neighborhood: str) -> list[str]:
    table = get_table("locations")
    neighborhood = table[
        table["cidade"].str.contains(city, regex=False)
        & table["bairro"].str.contains(neighborhood, regex=False)
    ]
    if neighborhood.empty:
        raise LocationNotFound()
    return neighborhood["bairro"].values.tolist()
