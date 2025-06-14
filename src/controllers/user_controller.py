from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List 
from fastapi import APIRouter, Depends 
from tokens.jwt_config import verify_token
from database.db import get_db  
from database.user_schema import User, UserCreate, UserDB, UserUpdate 
from services import users_service 
from exceptions import routes_error 

router = APIRouter(prefix="/users", include_in_schema=True, route_class= routes_error.RouteErrorHandler)  

@router.get('/all', response_model=List[User], dependencies=[Depends(verify_token)])
async def get_all(db: AsyncIOMotorDatabase = Depends(get_db)):
    list = await users_service.get_all(db)  
    return list

@router.get('/byname/{mPageNo}/{mPageSize}/{mUserName}', response_model=List[User], dependencies=[Depends(verify_token)])
async def by_name_users(mPageNo :int, mPageSize:int, mUserName:str, db = Depends(get_db)):
    return await users_service.byname_users(mPageNo , mPageSize, mUserName, db)

@router.post("/add_user", response_model=UserCreate, dependencies=[Depends(verify_token)])
async def create_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        return await users_service.add_user(user, db) 
    except PyMongoError as e:
        raise     

@router.put("/update_user/{id}", response_model=UserDB, dependencies=[Depends(verify_token)])
async def update_user(id: str, user: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        return await users_service.update_user(id, user, db) 
    except PyMongoError as e:
        raise  

@router.get("/user_details/{id}", response_model=User, dependencies=[Depends(verify_token)])
async def user_details(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        return await users_service.user_details(id, db) 
    except PyMongoError as e:
        raise 
    
@router.delete("/delete_user/{id}", dependencies=[Depends(verify_token)])
async def delete_user(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        return await users_service.delete_user(id, db) 
    except PyMongoError as e:
        raise   
    
