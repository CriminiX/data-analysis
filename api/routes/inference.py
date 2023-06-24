from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.shared import ScoreFilters, ReportOrientation
from schemas.responses import DefaultErrorResponse, ScoreReport
from exceptions import MissingRequiredValues
from services.inference import score, search
from services.location import LocationNotFound

router = APIRouter(prefix="/inference/v1")


@router.post("/score")
def create_score_report(filters: ScoreFilters, orient: ReportOrientation = ReportOrientation.AXES) -> ScoreReport | DefaultErrorResponse:
    try:
        return score(filters, orient)
    except LocationNotFound as e:
        resp = DefaultErrorResponse(summary="Location not found")
        return JSONResponse(jsonable_encoder(resp), 404)
    except MissingRequiredValues as e:
        resp = DefaultErrorResponse(summary=str(e), errors=e.values)
        return JSONResponse(jsonable_encoder(resp), 400)


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