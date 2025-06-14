from typing import cast
from fastapi.responses import FileResponse
import uvicorn 
from fastapi import FastAPI 
from exceptions import http_exception
from routers import routes
from middlewares import cors_middleware, file_middleware
from swagger import swagger_ui 
from config.settings import Settings 
settings = Settings()


#Swagger config
docs_url = f"/api/gateway" if settings.ENABLE_DOCS else None
redoc_url = f"/api/gateway/redocs" if settings.ENABLE_DOCS else None
openapi_url = f"/api/gateway/openapi.json" if settings.ENABLE_DOCS else None

#FastAPI init
app = FastAPI( 
    title= f"{settings.APP_NAME}",
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url)

favicon_name = "favicon.ico"
favicon_path = "static/images/" + favicon_name 

@app.get('/favicon.ico', include_in_schema=False)
def favicon(): 
    return FileResponse(favicon_path) 

# Register handlers & middlewares with the app 
http_exception.register_global_handlers(app)
cors_middleware.app_cors(app) 
file_middleware.mount_folder(app)
swagger_ui.add(app)

#Routes   
routes.all_routes(app) 
##breakpoint()
if __name__ == '__main__': 
    uvicorn.run("main:app", host=settings.HOST, port= settings.APP_PORT, reload=True, log_level="debug") 
