import warnings
import pandas as pd
from pathlib import Path

# from skl2onnx import convert_sklearn
# from skl2onnx.common.data_types import StringTensorType, Int32TensorType
from joblib import dump

from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn import tree

warnings.filterwarnings("ignore")

df = pd.read_csv("./notebooks/furtos_scored.csv")

max_points = df["pontos"].max()
df["pontos"] = df["pontos"] / max_points

basic = ["cidade", "bairro", "estacao", "periodo"]
with_date = [*basic, "mes", "dia", "hora"]
with_location = [*basic, "logradouro"]
full = [*basic, "logradouro", "mes", "dia", "hora"]

X_basic = df[basic]
X_with_date = df[with_date]
X_with_location = df[with_location]
X_full = df[full]

y = df["pontos"]


def _train(name, X, y):
    categorical = ["cidade", "bairro", "logradouro"]
    to_encode = [c for c in categorical if c in X.columns]

    one_hot_encoder = OneHotEncoder(drop="first", handle_unknown="ignore")
    preprocessing = ColumnTransformer(
        transformers=[
            (
                "categories",
                one_hot_encoder,
                to_encode,
            ),
        ],
        remainder="passthrough",
    )

    regressor = tree.DecisionTreeRegressor(
        max_depth=20, random_state=42, min_samples_leaf=100
    )

    pipeline = make_pipeline(preprocessing, regressor)
    pipeline.fit(X, y)
    Path("./models/score").mkdir(parents=True, exist_ok=True)
    dump(pipeline, f"./models/score/{name}.joblib")

    # initial_types = [
    #     ("cidade", StringTensorType([None, 1])),
    #     ("bairro", StringTensorType([None, 1])),
    #     ("logradouro", StringTensorType([None, 1])),
    #     ("descricaolocal", StringTensorType([None, 1])),
    #     ("mes", Int32TensorType([None, 1])),
    #     ("dia", Int32TensorType([None, 1])),
    #     ("hora", Int32TensorType([None, 1])),
    #     ("diasemana", Int32TensorType([None, 1])),
    # ]
    # onnx_model = convert_sklearn(pipeline, initial_types=initial_types, target_opset=12)

    # with open(f"./models/score/{name}.onnx", "+wb") as f:
    #     f.write(onnx_model.SerializeToString())


_train("score_basic", X_basic, y)
_train("score_with_date", X_with_date, y)
_train("score_with_location", X_with_location, y)
_train("score_full", X_full, y)
