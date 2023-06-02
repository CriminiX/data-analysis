from typing import List
from pydantic import BaseModel
from api.schemas.shared import Season, Location, Shift


class ScoreReportRecord(BaseModel):
    location: Location
    day: str | None
    shift: Shift
    season: Season
    score: float


class ScoreReportAxes(BaseModel):
    days: List[str] | None
    shifts: List[Shift]
    seasons: List[Season]
    locations: List[Location]
    scores: List[float]


class ScoreReport(BaseModel):
    records: List[ScoreReportRecord] | None
    axes: ScoreReportAxes | None


class DefaultErrorResponse(BaseModel):
    summary: str = "Something went wrong or the service is unavailable"
    errors: List[str] = []
