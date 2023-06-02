from typing import List
from api.schemas.shared import ScoreFilters, ReportOrientation, Location, Season, Shift
from api.schemas.responses import ScoreReport, ScoreReportAxes, ScoreReportRecord
from api.exceptions import MissingRequiredValues
from api.store.estimator_store import predict
from api.util import season_by_day, shift_by_hour
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

    has_date_fields = filters.day is not None and filters.hour is not None
    has_location_fields = filters.location.street is not None

    X = _to_experiment_list(filters)
    if has_date_fields and has_location_fields:
        scores = predict(X, "score_full")
    elif has_location_fields:
        scores = predict(X, "score_with_location")
    elif has_date_fields:
        scores = predict(X, "score_with_date")
    else:
        scores = predict(X, "score_basic")

    return _build_report(X, scores, orient)


def _to_experiment_list(score_filters: ScoreFilters):
    experiments = []
    data = score_filters.dict()
    if score_filters.period is not None:
        delta = score_filters.period.end - score_filters.period.begin
        for i in range(0, delta.days + 1):
            data["day"] = score_filters.period.begin + timedelta(days=i)
            experiments.append(_build_score_experiment(data.copy()))
    else:
        experiments.append(_build_score_experiment(data))

    return pd.DataFrame(experiments)


def _build_score_experiment(data: dict):
    if data["day"] is not None:
        data["season"] = season_by_day(data["day"])
    else:
        data["season"] = data["season"].to_code()

    if data["hour"] is not None:
        data["shift"] = shift_by_hour(data["hour"])
    else:
        data["shift"] = data["shift"].to_code()

    loc = data.get("location", {})
    day = data.get("day")
    return {
        "cidade": loc.get("city"),
        "bairro": loc.get("neighborhood"),
        "rua": loc.get("street"),
        "estacao": data.get("season"),
        "periodo": data.get("shift"),
        "mes": day.month if isinstance(day, date) else None,
        "dia": day.day if isinstance(day, date) else None,
        "hora": data.get("hour"),
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
