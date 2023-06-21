from pydantic import BaseSettings, DirectoryPath, FilePath
from functools import lru_cache


class Settings(BaseSettings):
    debug: bool = False
    model_path: DirectoryPath = "../models/score/scoreV2_full"
    location_table_path: FilePath = "../data/locations.csv"


@lru_cache(1)
def get_settings():
    return Settings()
