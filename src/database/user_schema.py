from datetime import datetime
from typing import Any, List, Optional  
from bson import ObjectId
from pydantic import BaseModel, Field, GetCoreSchemaHandler, ValidationInfo
from pydantic_core import core_schema

from database.enums import Role  

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        def validate(value: str, info: ValidationInfo) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        return core_schema.with_info_plain_validator_function(
            validate,
            serialization=core_schema.to_string_ser_schema(),
        )
        
# Users    
class User(BaseModel):   
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="id") # type: ignore
    username:str
    email:str 
    password:str   
    roles: List[Role] 
    tokens: str|None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    class Config:
        validate_by_name = True  
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
class UserCreate(User):    
    updatedAt: Optional[datetime] = Field(default=None, alias="updatedAt")  # New field, None on 
    pass
class UserDB(BaseModel):
    username:str 
    pass
            
class UserUpdate(BaseModel):
    username:str
    email:str 
    password:str   
    roles: List[Role] 
    tokens: str 
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
 
