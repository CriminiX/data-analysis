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