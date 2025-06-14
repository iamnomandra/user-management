from pymongo.errors import PyMongoError
from typing import List 
from fastapi import APIRouter, Depends  

from config.jwt_token import verify_token
from database.db import get_db  
from database.schemas import User, UserDB, UserUpdate 
from services import users_service 
from exceptions import routes_error

router = APIRouter(prefix="/users", include_in_schema=True, route_class= routes_error.RouteErrorHandler)  

@router.get('/all', response_model=List[User], dependencies=[Depends(verify_token)])
async def get_all(db = Depends(get_db)):
    list = await users_service.get_all(db)  
    return list

@router.get('/byname/{mPageNo}/{mPageSize}/{mUserName}', response_model=List[User], dependencies=[Depends(verify_token)])
async def by_name_users(mPageNo :int, mPageSize:int, mUserName:str, db = Depends(get_db)):
    return await users_service.byname_users(mPageNo , mPageSize, mUserName, db)

@router.post("/add_user", response_model=UserDB, dependencies=[Depends(verify_token)])
async def create_user(user: UserDB, db = Depends(get_db)):
    try:
        return await users_service.add_user(user, db) 
    except PyMongoError as e:
        raise     

@router.put("/update_user/{id}", response_model=UserDB, dependencies=[Depends(verify_token)])
async def update_user(id: str, user: UserUpdate, db = Depends(get_db)):
    try:
        return await users_service.update_user(id, user, db) 
    except PyMongoError as e:
        raise    

@router.delete("/delete_user/{id}", dependencies=[Depends(verify_token)])
async def delete_user(id: str, db = Depends(get_db)):
    try:
        return await users_service.delete_user(id, db) 
    except PyMongoError as e:
        raise   