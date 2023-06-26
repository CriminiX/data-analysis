from store.data_store import get_table
from schemas.shared import Location

class LocationNotFound(Exception):
    pass

def get_code_by_location(loc: Location) -> int | None:
    table = get_table("locations")
    neighborhood = table[(table["cidade"] == loc.city) & (table["bairro"] == loc.neighborhood)]
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