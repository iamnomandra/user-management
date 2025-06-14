from typing import List
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, IndexModel
from pymongo.errors import CollectionInvalid 
from exceptions import logger_init 

logger = logger_init.logging.getLogger(__name__)

def initialize_db(db: AsyncIOMotorClient, COLLECTIONS:  List[str]):
    try: 
        collection_names = db.collection_names
        existing_collections = collection_names 
        collection_name = set(COLLECTIONS) - set(existing_collections)  # type: ignore         
        db.create_collection(collection_name)      
        
        index_id = IndexModel([("id", ASCENDING)], unique=True)  
        indexes = [index_id]
        if collection_name == "users":
            index_email = IndexModel([("data.username", ASCENDING)], unique=True)
            indexes.append(index_email)        
        db[collection_name].create_indexes(indexes) # type: ignore
        
        logger.info(f"Created unique indexes for collection: {collection_name}")            
        return db
    except CollectionInvalid as e:
        logger.error(f"Creating collection: {f"Collection invalid: {str(e)}"}")
        raise HTTPException(status_code=500, detail=f"Failed to create collections: {str(e)}")
    except Exception as e: 
        return JSONResponse(
            status_code=500,
            content={"error": "Database error"}
        )

