from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from tokens.jwt_config import create_jwt_token, verify_token
from swagger.swagger_meta_tags import DESC, TAGS_META

from config.settings import Settings 
settings = Settings()

favicon_path = "static/images/favicon.ico" 
app_url =f"http://{settings.HOST}:{settings.APP_PORT}" 
appname = settings.APP_NAME

def add(app: FastAPI):
    @app.get("/api/gateway", include_in_schema=False)
    def custom_swagger_ui_html(): 
        return get_swagger_ui_html(openapi_url= app.openapi_url,  # type: ignore
        title=f"{appname}: API", 
        swagger_favicon_url = favicon_path)
        
    def custom_openapi():
        try: 
            app.openapi_schema = get_openapi(title=f"{appname}: API", 
            version = f"{settings.APP_VERSION}",   
            openapi_version = "3.1.0",                                
            description = DESC, 
            routes = app.routes,
            tags = TAGS_META,             
            terms_of_service = f"{app_url}/terms/",
                contact = {
                    "name": "Amit Kumar",
                    "url": f"{app_url}/contact/",
                    "email": "iamnomandra@gmail.com",
                },
                license_info = {
                    "name": "License Apache 2.0",
                    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                },
                separate_input_output_schemas= True, 
            )  
        except Exception as ex: 
            print(ex.args) 
        return app.openapi_schema
    app.openapi = custom_openapi # type: ignore
    
    @app.get("/api/gateway/redocs", include_in_schema=False)
    def overridden_redoc():
        return get_redoc_html(openapi_url= app.openapi_url,  # type: ignore
        title=f"{appname}: API Docs", 
        redoc_favicon_url=favicon_path,
        redoc_js_url="/static/js/redoc.standalone.js")
        
    