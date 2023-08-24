from typing import Annotated
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.responses import DefaultErrorResponse
from exceptions import MissingRequiredValues
from services.location import search
from services.location import LocationNotFound
import util

router = APIRouter(prefix="/location/v1")

@router.get("/search")
async def read_item(
    city: str | None = None, 
    neighborhood: str | None = None, 
    zip_code: Annotated[str | None, Query(regex=util.NUMBERS_ONLY)] = None
):
    try:
        return search(city, neighborhood, zip_code)
    except LocationNotFound as e:
        resp = DefaultErrorResponse(summary="Location not found")
        return JSONResponse(jsonable_encoder(resp), 404)
    except MissingRequiredValues as e:
        resp = DefaultErrorResponse(summary=str(e), errors=e.values)
        return JSONResponse(jsonable_encoder(resp), 400)
