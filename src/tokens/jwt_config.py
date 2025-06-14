from fastapi import Depends, HTTPException , status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  
from jose import jwt, JWTError
from datetime import datetime, timedelta


from config.settings import Settings 
settings = Settings() 

bearer_scheme = HTTPBearer()

def create_jwt_token(module: int, apikey: str):
    if module != settings.TOKEN_MODULE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please enter valid module!!!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if apikey != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please enter valid api key!!!",
            headers={"WWW-Authenticate": "Bearer"},
        )    
        
    expiry= datetime.utcnow() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    
    token_load={
            "module": module, 
            "sub": "iamnomandra", 
            "apikey":apikey,
            "iat": datetime.now(),
            "exp": expiry 
    }
    token = jwt.encode(token_load, settings.SECRET_KEY, algorithm=settings.ALGORITHM) 
    return token
    

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) 
        sub = payload.get("sub")
        module = payload.get("module")
        apikey = payload.get("apikey")        
        if apikey is None:
            raise HTTPException(status_code=401, detail="Invalid JWT payload")             
        if module != settings.TOKEN_MODULE:
            raise HTTPException(status_code=401, detail="Invalid JWT payload")            
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid JWT payload")
        return sub
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )







