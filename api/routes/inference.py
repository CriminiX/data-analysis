from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from api.schemas.shared import ScoreFilters, ReportOrientation
from api.schemas.responses import DefaultErrorResponse, ScoreReport
from api.exceptions import MissingRequiredValues
from api.services.inference import score

router = APIRouter(prefix="/inference/v1")


@router.post("/score")
def create_score_report(filters: ScoreFilters, orient: ReportOrientation = ReportOrientation.AXES) -> ScoreReport | DefaultErrorResponse:
    try:
        return score(filters, orient)
    except MissingRequiredValues as e:
        resp = DefaultErrorResponse(summary=str(e), errors=e.values)
        return JSONResponse(jsonable_encoder(resp), 400)
