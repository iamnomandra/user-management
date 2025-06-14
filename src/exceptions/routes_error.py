from typing import Callable, Coroutine 
from typing import Any 
from fastapi import Request, Response 
from pymongo.errors import PyMongoError
from fastapi.routing import APIRoute
from exceptions import logger_init 

logger = logger_init.logging.getLogger(__name__)
class RouteErrorHandler(APIRoute):
    """Custom APIRoute that handles application errors and exceptions"""

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except PyMongoError as e:
                raise  # Let the global handler catch this 

        return custom_route_handler