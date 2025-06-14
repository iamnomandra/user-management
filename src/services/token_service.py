from pymongo.errors import PyMongoError 
from fastapi import HTTPException

from tokens.jwt_config import create_jwt_token 
from database.token_schema import Token
from config.settings import Settings 
settings = Settings()


def get_token(model: Token):
    try:
        # if not model.username or not model.token_module:
        #     raise HTTPException(status_code=400, detail="User name/password is missing!!!")
        if(model.token_module == settings.TOKEN_MODULE and model.apikey == settings.API_KEY):
            return {"access_token": create_jwt_token(model.token_module, model.apikey)}
        else:
            raise HTTPException(status_code=500, detail="You are not authorized!!!") 
    except PyMongoError as e:
        raise  # Let the global handler catch this 
