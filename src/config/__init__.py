from .settings import Settings
from .cors_config import Settings as Cors
init_setting = Settings()
__all__ = ['init_setting', "Cors"]