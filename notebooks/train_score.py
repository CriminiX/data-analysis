import warnings
import pandas as pd

warnings.filterwarnings('ignore')

df = pd.read_csv("./notebooks/furtos_consolidado.csv")
crimes = df[["DATAOCORRENCIA", "HORAOCORRENCIA", "CIDADE", "BAIRRO", "LOGRADOURO", "DESCRICAOLOCAL"]]
crimes["DATAHORA"] = pd.to_datetime(crimes["DATAOCORRENCIA"] + " " + crimes["HORAOCORRENCIA"])
crimes.drop(columns=["DATAOCORRENCIA", "HORAOCORRENCIA"], inplace=True)
crimes.dropna(inplace=True)

categorical_cols = ["CIDADE", "BAIRRO", "LOGRADOURO", "DESCRICAOLOCAL"]
for c in categorical_cols:
  crimes.loc[:, c] = crimes[c].str.normalize("NFKD").str.encode("ascii",  errors='ignore').str.decode("UTF-8").str.lower()

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

print(crimes_sp.shape)
print(crimes_remaining.shape)

from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn import tree

def _train(name, crimes):
    X, y = crimes.iloc[:, :-1].values, crimes.iloc[:, -1].values

    one_hot_encoder = OneHotEncoder(drop="first")
    preprocessing = ColumnTransformer(transformers=[
        ("categories", one_hot_encoder, [0, 1, 2, 3])
    ], remainder="passthrough")

    regressor = tree.DecisionTreeRegressor(
        max_depth=20,
        random_state=42,
        min_samples_leaf=100
    )

    pipeline = make_pipeline(preprocessing, regressor)
    pipeline.fit(X, y)

    from joblib import dump
    dump(pipeline, f"./models/score/{name}.joblib")

    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import StringTensorType, Int32TensorType

    initial_types = [
        ("categories", StringTensorType([None, 4])),
        ("numbers", Int32TensorType([None, 4])),
    ]
    onnx_model = convert_sklearn(pipeline, initial_types=initial_types)
    with open(f"./models/score/{name}.onnx", "+wb") as f:
        f.write(onnx_model.SerializeToString())

_train("score_sp", crimes_sp)
_train("score_remaining", crimes_remaining)