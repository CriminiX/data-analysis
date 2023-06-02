from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class ReportOrientation(str, Enum):
    AXES = "AXES"
    RECORDS = "RECORDS"


_season_mappings = {
    "SUMMER": 1,
    "AUTUMN": 2,
    "WINTER": 3,
    "SPRING": 4,
}
_season_codes = list(_season_mappings.values())
_season_labels = list(_season_mappings.keys())


class Season(str, Enum):
    SUMMER = "SUMMER"
    AUTUMN = "AUTUMN"
    WINTER = "WINTER"
    SPRING = "SPRING"

    def to_code(self):
        return _season_mappings[self.value]

    @classmethod
    def from_code(cls, code):
        i = _season_codes.index(code)
        return _season_labels[i]


_shift_mappings = {"DAWN": 0, "MORNING": 1, "NIGHT": 2}
_shift_codes = list(_shift_mappings.values())
_shift_labels = list(_shift_mappings.keys())


class Shift(str, Enum):
    DAWN = "DAWN"
    MORNING = "MORNING"
    NIGHT = "NIGHT"

    def to_code(self):
        return _shift_mappings[self.value]

    @classmethod
    def from_code(cls, code):
        i = _shift_codes.index(code)
        return _shift_labels[i]


class Location(BaseModel):
    city: str = Field(description="A target city, if unknown will return an error")
    neighborhood: str = Field(
        description="A target neighborhood, if unknown will return an error"
    )
    street: str | None = Field(
        description="A target street, if unknown will return an error"
    )


class PeriodFilter(BaseModel):
    begin: date = Field(
        description="The first day of the period, in the format YYYY-MM-DD",
        example="2023-02-01",
    )
    end: date = Field(
        description="The last day of the period, in the format YYYY-MM-DD",
        example="2023-02-31",
    )


class ScoreFilters(BaseModel):
    location: Location
    shift: Shift | None
    hour: int | None = Field(description="A hour filter")
    day: date | None = Field(
        description="A target day, in the format YYYY-MM-DD", example="2023-02-01"
    )
    season: Season | None = Field(
        description="The analised season, defined as: summer = 1, autumn = 2, winter = 3, spring = 4"
    )
    period: PeriodFilter | None
