import os
from joblib import load
import pandas as pd
from sklearn.base import BaseEstimator
import numpy as np

class ModelNotFound(Exception):
    pass

models = {}

def get_estimator(name: str) -> BaseEstimator:
    m = models.get(name)
    if m is None:
        raise ModelNotFound()
    return m


def register_estimator(name: str, path: str) -> None:
    if not os.path.exists(path):
        raise ModelNotFound()
    m = load(path)
    models[name] = m


def predict(X: pd.DataFrame, model_name: str) -> np.ndarray:
    m = get_estimator(model_name)
    return m.predict(X)
