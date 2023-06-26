from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import inference, location
from store.estimator_store import register_estimator
from store.data_store import register_table
from util import get_logger, clone_log_config
from tensorflow import keras
import logging
from settings import get_settings

logger = get_logger(__file__)

server_logger = logging.getLogger("uvicorn")
clone_log_config(logger, server_logger)
server_logger = logging.getLogger("uvicorn.access")
clone_log_config(logger, server_logger)
server_logger = logging.getLogger("uvicorn.error")
clone_log_config(logger, server_logger)

keras.utils.disable_interactive_logging()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app = FastAPI()
app.include_router(inference.router)
app.include_router(location.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=True,
)


@app.on_event("startup")
async def load_stores():
    settings = get_settings()
    register_estimator("score_full", settings.model_path)
    register_table("locations", settings.location_table_path)
