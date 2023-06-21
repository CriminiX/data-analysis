import os
from joblib import load
import pandas as pd
from tensorflow import keras
from functools import lru_cache
import numpy as np

class ModelNotFound(Exception):
    pass

models = {}

@lru_cache(1)
def get_estimator(name: str) -> keras.Model:
    path = models.get(name)
    if path is None:
        raise ModelNotFound()
    return keras.models.load_model(path)


def register_estimator(name: str, path: str) -> None:
    if not os.path.exists(path):
        raise ModelNotFound()
    models[name] = path


def predict(X: pd.DataFrame, model_name: str) -> np.ndarray:
    m = get_estimator(model_name)
    return m.predict(X)
