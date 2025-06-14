from fastapi import APIRouter
from database.token_schema import Token
from exceptions import routes_error
from services import token_service

router = APIRouter(prefix="/tokens", include_in_schema=True, route_class= routes_error.RouteErrorHandler)  

@router.post("/get_token/")
def get_token(model: Token):
    return token_service.get_token(model) 