from typing import List
from schemas.shared import ScoreFilters, ReportOrientation, Location, Season, Shift
from schemas.responses import ScoreReport, ScoreReportAxes, ScoreReportRecord
from exceptions import MissingRequiredValues
from services.location import get_code_by_location, get_neighborhood
from store.estimator_store import predict
from util import season_by_day, sin_transform, cos_transform
from datetime import timedelta, date
import pandas as pd


def score(filters: ScoreFilters, orient: ReportOrientation):
    missing = []
    if filters.season is None and filters.day is None and filters.period is None:
        missing.append("missing one of: season or day or period")
    if filters.shift is None and filters.hour is None:
        missing.append("missing one of: shift or hour")
    if missing:
        raise MissingRequiredValues(missing)

    exp = _build_experiments(filters)
    X = _to_features(exp)
    scores = predict(X, "score_full")

    return _build_report(exp, scores, orient)


def _build_experiments(score_filters: ScoreFilters):
    experiments = []
    code = get_code_by_location(score_filters.location)
    data = score_filters.dict()
    data["location_code"] = code
    if score_filters.period is not None:
        delta = score_filters.period.end - score_filters.period.begin
        for i in range(delta.days + 1):
            data["day"] = score_filters.period.begin + timedelta(days=i)
            experiments.append(_build_score_experiment(data.copy()))
    else:
        experiments.append(_build_score_experiment(data))

    return pd.DataFrame(experiments)


def _to_features(experiments: pd.DataFrame):
    X = experiments.copy()

    X["mes_sin"] = sin_transform(X["mes"], 12)
    X["mes_cos"] = cos_transform(X["mes"], 12)
    X["dia_sin"] = sin_transform(X["dia"], 30)
    X["dia_cos"] = cos_transform(X["dia"], 30)
    
    X = X.drop(columns=["cidade", "bairro", "rua", "mes", "dia"])
    return {
        "location_code": X["location_code"],
        "date_features": X.drop(columns=["location_code"]),
    }


def _build_score_experiment(data: dict):
    if data["day"] is not None:
        data["season"] = season_by_day(data["day"])
    else:
        data["season"] = data["season"].to_code()

    data["shift"] = data["shift"].to_code()

    loc = data.get("location", {})
    day = data.get("day")
    return {
        "cidade": loc.get("city"),
        "bairro": loc.get("neighborhood"),
        "rua": loc.get("street"),
        "location_code": data.get("location_code"),
        "estacao": data.get("season"),
        "ano": day.year if isinstance(day, date) else None,
        "mes": day.month if isinstance(day, date) else None,
        "dia": day.day if isinstance(day, date) else None,
        "periodo": data.get("shift"),
    }


def _build_report(
    experiments: pd.DataFrame, results: List[int], orient: ReportOrientation
):
    experiments["mes"] = experiments["mes"].astype("string").str.pad(2, "left", "0")
    experiments["dia"] = experiments["dia"].astype("string").str.pad(2, "left", "0")
    experiments["periodo"] = experiments["periodo"].apply(Shift.from_code)
    experiments["estacao"] = experiments["estacao"].apply(Season.from_code)
    data = experiments.assign(score=results)
    if orient == ReportOrientation.AXES:
        return _build_axes_report(data)
    else:
        return _build_records_report(data)


def _build_axes_report(data: pd.DataFrame):
    days = (data["mes"] + "-" + data["dia"]).tolist()
    locations = (
        data[["cidade", "bairro", "rua"]]
        .apply(lambda r: Location(city=r[0], neighborhood=r[1], street=r[2]), axis=1)
        .tolist()
    )
    shifts = data["periodo"].tolist()
    seasons = data["estacao"].tolist()
    scores = data["score"].tolist()
    axes = ScoreReportAxes(
        days=days, locations=locations, shifts=shifts, seasons=seasons, scores=scores
    )
    return ScoreReport(axes=axes)


def _build_records_report(data: pd.DataFrame):
    records = []
    rows = data.to_dict("records")
    for rw in rows:
        mes, dia = rw.get("mes"), rw.get("dia")
        day = "-".join([mes, dia])
        loc = Location(
            city=rw.get("cidade"),
            neighborhood=rw.get("bairro"),
            street=rw.get("rua"),
        )
        records.append(
            ScoreReportRecord(
                location=loc,
                day=day,
                shift=rw.get("periodo"),
                season=rw.get("estacao"),
                score=rw.get("score"),
            )
        )
    return ScoreReport(records=records)

def search(city: str, neighborhood: str):
    data_list_city = []
    data_list_neighborhood = []

    if city is not None:
        data = get_neighborhood(city.lower())
        data_list_city = list(dict.fromkeys(data))

    if neighborhood is not None:
        data = get_neighborhood(neighborhood.lower())
        data_list_neighborhood = list(dict.fromkeys(data))

    return {
        'cidades': data_list_city,
        'bairros': data_list_neighborhood
    }
