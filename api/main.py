from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import inference
from api.store.estimator_store import register_estimator
import glob
from api.util import get_logger, clone_log_config
import logging
from api.settings import get_settings

logger = get_logger(__file__)

server_logger = logging.getLogger("uvicorn")
clone_log_config(logger, server_logger)
server_logger = logging.getLogger("uvicorn.access")
clone_log_config(logger, server_logger)
server_logger = logging.getLogger("uvicorn.error")
clone_log_config(logger, server_logger)

origins = ["*"]
methods = ["*"]
headers = ["*"]

app = FastAPI()
app.include_router(inference.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=True
)

@app.on_event("startup")
async def load_estimators():
    settings = get_settings()
    model_list = glob.glob(f"{settings.models_path}/**/*.joblib", recursive=True)
    if not model_list:
        logger.warning("No model was found")

    for m in model_list:
        name = m.split("/")[-1].split(".")[0]
        register_estimator(name, m)
        logger.info("Registered model: %s", name)
