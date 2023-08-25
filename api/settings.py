from pydantic import BaseSettings, DirectoryPath, FilePath
from functools import cache


class Settings(BaseSettings):
    debug: bool = False
    model_path: DirectoryPath = "../models/score/scoreV2_full"
    location_table_path: FilePath = "../data/locations2.csv"


@cache
def get_settings():
    return Settings()
