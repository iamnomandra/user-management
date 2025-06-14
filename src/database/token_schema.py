import base64
from pydantic import BaseModel, field_validator
import base64
import re

class Token(BaseModel):
    apikey:str  
    token_module:int  

    @field_validator("apikey")
    def validate_apikey(cls, v: str) -> str:
        # Regular expression for base64 (allows padding with =)
        base64_pattern = r'^[A-Za-z0-9+/]+={0,2}$'
        if not re.match(base64_pattern, v):
            raise ValueError("API key must be a valid api key")
        
        # Optionally, verify by decoding (ensures it's valid base64)
        try:
            # Ensure length is divisible by 4 (valid base64 length)
            if len(v) % 4 != 0:
                raise ValueError
            base64.b64decode(v, validate=True)
        except ValueError as e:
            raise ValueError("Invalid api key.")        
        return v