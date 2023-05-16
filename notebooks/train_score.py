import pandas as pd
import glob
import numpy as np

df = pd.read_csv("furtos_consolidado.csv")
crimes = df[["DATAOCORRENCIA", "HORAOCORRENCIA", "CIDADE", "BAIRRO", "LOGRADOURO", "DESCRICAOLOCAL"]]
crimes["DATAHORA"] = pd.to_datetime(crimes["DATAOCORRENCIA"] + " " + crimes["HORAOCORRENCIA"])
crimes.drop(columns=["DATAOCORRENCIA", "HORAOCORRENCIA"], inplace=True)
crimes.dropna(inplace=True)

crimes["DATA"] = crimes["DATAHORA"].dt.date
crimes["ANO"] = crimes["DATAHORA"].dt.year
crimes["MES"] = crimes["DATAHORA"].dt.month
crimes["DIA"] = crimes["DATAHORA"].dt.day
crimes["HORA"] = crimes["DATAHORA"].dt.hour
crimes["DIASEMANA"] = crimes["DATAHORA"].dt.weekday

to_score = ["CIDADE", "BAIRRO", "LOGRADOURO", "DATA", "HORA"]
for t in to_score:
  grouped = crimes.groupby(t).size().reset_index()
  grouped.rename(columns={0: f"{t}_PONTOS"}, inplace=True)
  crimes = crimes.join(grouped.set_index(t), on=t)

scores = ["CIDADE_PONTOS", "BAIRRO_PONTOS", "LOGRADOURO_PONTOS", "DATA_PONTOS", "HORA_PONTOS"]
crimes["PONTOS"] = crimes[scores].sum(axis=1)

crimes.drop(columns=["DATAHORA", "ANO", "DATA", *scores], inplace=True)

min_points = crimes["PONTOS"].min()
max_points = crimes["PONTOS"].max()
crimes["PONTOS"] = (crimes["PONTOS"] - min_points) / (max_points - min_points)

crimes = crimes.reindex(columns=[
    'CIDADE', 'BAIRRO', 'LOGRADOURO', 'DESCRICAOLOCAL', 'MES',
    'DIA', 'HORA', 'DIASEMANA', 'PONTOS'
])

crimes_sp = crimes[crimes["CIDADE"] == "s.paulo"]
crimes_remaining = crimes[crimes["CIDADE"] != "s.paulo"]

from sklearn.preprocessing import SplineTransformer, OneHotEncoder, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn import tree

def periodic_spline_transformer(period, n_splines=None, degree=3):
    if n_splines is None:
        n_splines = period
    n_knots = n_splines + 1  # periodic and include_bias is True
    return SplineTransformer(
        degree=degree,
        n_knots=n_knots,
        knots=np.linspace(0, period, n_knots).reshape(n_knots, 1),
        extrapolation="periodic",
        include_bias=True,
    )

X, y = crimes.iloc[:, :-1].values, crimes.iloc[:, -1].values

one_hot_encoder = OneHotEncoder(drop="first")
preprocessing = ColumnTransformer(transformers=[
    ("categories", one_hot_encoder, [0, 1, 2, 3]),
    ("month", periodic_spline_transformer(12, 6), [4]),
    ("day", periodic_spline_transformer(365, 182), [5]),
    ("hour", periodic_spline_transformer(24, 12), [6]),
    ("weekday", periodic_spline_transformer(7, 3), [7])
], remainder="drop")

regressor = tree.DecisionTreeRegressor(
    max_depth=20,
    random_state=42,
    min_samples_leaf=100
)

pipeline = make_pipeline(preprocessing, regressor)
pipeline.fit(X, y)

from joblib import dump
dump(pipeline, "./models/score_sp.joblib")

#TODO - Add sklearn-onnx