from datetime import datetime
from typing import List 
from bson import ObjectId
from fastapi import Depends, HTTPException 
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorDatabase

from database.user_schema import User, UserCreate, UserUpdate

# Dependency to get MongoDB database

async def get_all(db: AsyncIOMotorDatabase) -> List[dict]:
    try:
        users_cursor = db["users"].find({})
        users = await users_cursor.to_list()
        return users  
    except PyMongoError as e:
        raise  # Let the global handler catch this 
    
async def byname_users(mPageNo: int, mPageSize: int, mUserName: str, db: AsyncIOMotorDatabase) -> List[dict]: 
    try:
        skip = (mPageNo - 1) * mPageSize 
        mlist = db["users"].find({"username": {"$regex": mUserName, "$options": "i"}})\
                        .skip(skip)\
                        .limit(mPageSize)
        return await mlist.to_list(length=mPageSize)      
    except PyMongoError as e:
        raise  # Let the global handler catch this 

async def add_user(user: UserCreate, db: AsyncIOMotorDatabase)->User:
    try: 
        # Check if user already exists
        existing_user = await db["users"].find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        user_dict = user.model_dump(by_alias=True)
        user_dict["createdAt"] = datetime.now()
        result = await db["users"].insert_one(user_dict)
        created_user = await db["users"].find_one({"id": result.inserted_id})
        if created_user is None:
            raise HTTPException(status_code=500, detail="User created but could not be retrieved")
        
        return created_user   
    except PyMongoError as e:
        raise  # Let the global handler catch this  
    
async def update_user(id: str, user: UserUpdate,  db: AsyncIOMotorDatabase):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        # Check for duplicate email (excluding current user)
        existing_user_by_email = await db["users"].find_one({"email": user.email, "id": {"$ne": ObjectId(id)}})
        if existing_user_by_email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
        # Update document with new data and current timestamp
        user_dict = user.dict(by_alias=True, exclude_unset=True)
        user_dict["updatedAt"] = datetime.utcnow()  # Set updatedAt to current timestamp    
        
        result = await db["users"].update_one(
            {"id": ObjectId(id)},
            {"$set": user_dict}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        updated_user = await db["users"].find_one({"id": ObjectId(id)})
        if updated_user is None:
            raise HTTPException(status_code=500, detail="User updated but could not be retrieved")
        
        return updated_user
    except PyMongoError as e:
        raise  # Let the global handler catch this 

async def user_details(id: str, db: AsyncIOMotorDatabase)-> User:
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid user ID")         
        _user = await db["users"].find_one({"id": ObjectId(id)})
        if not _user:
            raise HTTPException(status_code=400, detail="User not found") 
        _user["id"] = str(_user["_id"])  # Convert ObjectId to string
        del _user["_id"]  # Remove _id for schema  security 
        return User(**_user)  
    except PyMongoError as e:
        raise  # Let the global handler catch this 

async def delete_user(user_id: str,  db: AsyncIOMotorDatabase):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        result = await db["users"].delete_one({"id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except PyMongoError as e:
        raise  # Let the global handler catch this 
    
    