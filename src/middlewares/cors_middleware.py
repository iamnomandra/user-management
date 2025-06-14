from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.cors_config import Settings
import logging


logger = logging.getLogger(__name__)
settings= Settings()

def app_cors(app: FastAPI):
    origins = settings.all_cors_origins 

    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        msg = f"CORS enabled for origins: {origins}" 
        logger.info(msg)
    else:
        logger.warning("CORS not applied — no origins configured")    