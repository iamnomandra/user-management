from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import  ValidationError
from typing import Awaitable, Callable,  Any 
from pymongo.errors import DuplicateKeyError, PyMongoError
from exceptions import logger_init 

logger = logger_init.logging.getLogger(__name__) 
 
# Class for global error handling
class GlobalErrorHandler:
    @staticmethod
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

    @staticmethod
    async def handle_validation_error(request: Request, exc: ValidationError) -> JSONResponse:
        logger.warning(f"Validation error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid input data", "details": exc.errors()}
        )

    @staticmethod
    async def handle_pymongo_error(request: Request, exc: PyMongoError) -> JSONResponse:
        logger.error(f"MongoDB error: {str(exc)}")
        if isinstance(exc, DuplicateKeyError):
            return JSONResponse(
                status_code=400,
                content={"error": exc.args}
            )
        return JSONResponse(
            status_code=500,
            content={"error": "Database error"}
        )

    @staticmethod
    async def handle_generic_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Unexpected error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"{str(exc)}"}
        )

# Define ExceptionHandler type
ExceptionHandler = Callable[[Request, Exception], Awaitable[Response]]

# Wrapper functions with broader type hints
async def http_exception_handler(request: Request, exc: Exception) -> Response:
    logger.debug(f"Invoking http_exception_handler for {exc}")
    if not isinstance(exc, HTTPException):
        raise exc  # Re-raise if not the expected type
    return await GlobalErrorHandler.handle_http_exception(request, exc)

async def validation_exception_handler(request: Request, exc: Exception) -> Response:
    if not isinstance(exc, ValidationError):
        logger.debug(f"Invoking validation_exception_handler for {exc}")
        raise exc
    return await GlobalErrorHandler.handle_validation_error(request, exc)

async def pymongo_exception_handler(request: Request, exc: Exception) -> Response:
    if not isinstance(exc, PyMongoError):
        logger.debug(f"Invoking pymongo_exception_handler for {exc}")
        raise exc
    return await GlobalErrorHandler.handle_pymongo_error(request, exc)

async def generic_exception_handler(request: Request, exc: Exception) -> Response:
    logger.debug(f"Invoking generic_exception_handler for {exc}")
    return await GlobalErrorHandler.handle_generic_exception(request, exc)

# Wrapper functions with explicit type hints
ExceptionHandlerType = Callable[[Request, Any], Awaitable[Response]]

# Register global error handlers
def register_global_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(PyMongoError, pymongo_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler) 


'''''
# Register global error handlers with logger
app.add_exception_handler(HTTPException, partial(GlobalErrorHandler.handle_http_exception, logger=logger))
app.add_exception_handler(ValidationError, partial(GlobalErrorHandler.handle_validation_error, logger=logger))
app.add_exception_handler(PyMongoError, partial(GlobalErrorHandler.handle_pymongo_error, logger=logger))
app.add_exception_handler(Exception, partial(GlobalErrorHandler.handle_generic_exception, logger=logger))


try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Test connection
 except PyMongoError as e:
        raise  # Let the global handler catch this
'''

