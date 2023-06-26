from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.responses import DefaultErrorResponse
from exceptions import MissingRequiredValues
from services.location import search
from services.location import LocationNotFound

router = APIRouter(prefix="/location/v1")

@router.get("/search")
async def read_item(city: str | None = None, neighborhood: str | None = None):
    try:
        return search(city, neighborhood)
    except LocationNotFound as e:
        resp = DefaultErrorResponse(summary="Location not found")
        return JSONResponse(jsonable_encoder(resp), 404)
    except MissingRequiredValues as e:
        resp = DefaultErrorResponse(summary=str(e), errors=e.values)
        return JSONResponse(jsonable_encoder(resp), 400)
