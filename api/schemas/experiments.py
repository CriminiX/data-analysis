from pydantic import BaseModel
from schemas.shared import ScoreFilters


class ScoreExperiment(BaseModel):
    cidade: str
    bairro: str
    estacao: str
    periodo: str
    mes: int
    dia: int
    hora: int
    logradouro: str

    @classmethod
    def from_filters(cls, filters: ScoreFilters):
        return ScoreExperiment(
            cidade=filters.location.city,
            bairro=filters.location.neighborhood,
            estacao=filters.season,
            periodo=filters.shift,
            mes=filters.day.month,
            dia=filters.day.day,
            hora=filters.hour,
            logradouro=filters.location.street,
        )
