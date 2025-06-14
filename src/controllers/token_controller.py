from fastapi import APIRouter
from config.jwt_token import create_jwt_token
from exceptions import routes_error

router = APIRouter(prefix="/tokens", include_in_schema=True, route_class= routes_error.RouteErrorHandler)  

@router.get("/token/{model}/{user}")
def get_token(model:int, user: str):
    return {"access_token": create_jwt_token(model, user)}