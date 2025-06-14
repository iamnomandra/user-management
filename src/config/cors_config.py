from typing import Annotated, Any
from pydantic import AnyUrl, BeforeValidator, computed_field
from config.settings import Settings as Cors

settings = Cors()

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)

class Settings(): 
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        origins = [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS if origin] 
        if settings.FRONTEND_HOST:
            origins.extend(settings.FRONTEND_HOST)  
        return origins
