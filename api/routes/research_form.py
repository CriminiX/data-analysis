from typing import Annotated
from fastapi import APIRouter, Query, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schemas.responses import DefaultErrorResponse
from exceptions import MissingRequiredValues, TheValueAlreadyExists
import util
from services.research_form import insert_research_form
from schemas.responses import ResearchBody

router = APIRouter(prefix="/research/v1")

@router.post("/response-user")
async def save_response_from_user(body: ResearchBody, criminix_id: str = Header(..., convert_underscores=True)):
    try:
        insert_research_form(body.scores, 
                             body.cities, 
                             body.neighborhoods, 
                             body.satisfaction_rate, 
                             body.suggestion_scores,
                             body.is_work_insurance,
                             body.obversation, 
                             criminix_id)
        return JSONResponse(jsonable_encoder({ "message": "answer registered successfully" }), 201)
    except MissingRequiredValues as e:
        resp = DefaultErrorResponse(summary=str(e), errors=e.values)
        return JSONResponse(jsonable_encoder(resp), 400)
    except TheValueAlreadyExists as e:
        resp = DefaultErrorResponse(summary=str(e), errors=e.values)
        return JSONResponse(jsonable_encoder(resp), 400)
    

