from typing import cast
from fastapi import FastAPI
from config.settings import Settings

settings = Settings()
from controllers import token_controller as token 
from controllers import user_controller as user 
def all_routes(app: FastAPI): 
    app.include_router(token.router, prefix= settings.API_V1_STR, tags= ["Tokens"]) 
    app.include_router(user.router, prefix= settings.API_V1_STR, tags= ["Users"]) 