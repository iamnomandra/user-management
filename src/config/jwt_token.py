from fastapi import Depends, HTTPException , status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  
from jose import jwt, JWTError
from datetime import datetime, timedelta


from config.settings import Settings 
settings = Settings() 

bearer_scheme = HTTPBearer()

def create_jwt_token(module: int, user: str):
    if module != settings.TOKEN_MODULE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please enter valid module!!!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    expiry= datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_load={
            "module": module, 
            "sub": user, 
            "iat": datetime.now(),
            "exp": expiry 
    }
    return jwt.encode(token_load, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        module = payload.get("module")
        if module != settings.TOKEN_MODULE:
            raise HTTPException(status_code=401, detail="Invalid JWT payload")            
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid JWT payload")
        return username
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )







