import os
import pandas as pd

class TableNotFound(Exception):
    pass

tables = {}

def get_table(name: str):
    t = tables.get(name)
    if t is None:
        raise TableNotFound()
    
    return pd.read_csv(t)

def register_table(name: str, path: str) -> None:
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError()
    
    tables[name] = path
