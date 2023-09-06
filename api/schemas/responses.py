from datetime import date
from typing import List
from pydantic import BaseModel
from schemas.shared import Season, Location, Shift


class ScoreReportRecord(BaseModel):
    location: Location
    day: date | None
    shift: Shift
    season: Season
    score: float


class ScoreReportAxes(BaseModel):
    days: List[date] | None
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

class LocationRef(BaseModel):
    city: str | None
    neighborhood: str | None
    zip_code : str | None

class LocationSearchResponse(BaseModel):
    records: List[LocationRef]

class ResearchBody(BaseModel):
    scores: list[str]
    cities: list[str]
    neighborhoods: list[str]
    satisfaction_rate: int
    obversation: str | None