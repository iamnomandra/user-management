import socket
from pydantic_settings import BaseSettings

host = socket.gethostbyname(socket.gethostname())

class Settings(BaseSettings): # type: ignore
    ENABLE_DOCS: bool=True  
    HOST: str="127.0.0.1" if (host == "172.4.195.66" or host == "192.168.29.48") else host
    APP_VERSION: str="0.1.0" 
    APP_NAME: str ="User Management" 
    API_V1_STR: str="/api/v1"
    APP_PORT: int=8000
    TOKEN_MODULE: int=20250610
    API_DESCRIPTION: str="API DESCRIPTION"
    API_VERSION: str="1.0.0"
    FRONTEND_HOST: list[str]= ["http://localhost.tiangolo.com", "https://localhost.tiangolo.com"]
    MONGO_STRING: str="mongodb://localhost:27017"
    DATABASE_NAME: str="fastapi-mongo-api"
    SECRET_KEY: str=  "UEK0sZLsQUTnY0a3drLvJTcneoOZSckXb8AyYRgpbbe6OqQ9i2yPxuu0g69aTvtUKsB7S1wZoKBy7iEpDHbY4A=="
    ALGORITHM: str= "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 10
    POWERED_BY: str="iamomandra"
    API_KEY:str ="ofxH3NSHE/Hs6uRkeMspPVqpnde5U8KhZ2FfCMZbuCE="

    class Config:
        env_file = ".env"