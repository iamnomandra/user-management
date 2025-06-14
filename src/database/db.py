from typing import Annotated 
from fastapi import Depends 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pymongo.errors import PyMongoError 

from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import Settings

settings = Settings()
TABLE_COLLECTIONS = ["users"]
from database.ini_database import initialize_db
Base = declarative_base() 
client = AsyncIOMotorClient(settings.MONGO_STRING) 

getdb = client[settings.DATABASE_NAME] 

# Initialize collection
try:
    collection = initialize_db(client, TABLE_COLLECTIONS) 
except PyMongoError as e:
        raise  # Let the global handler catch this
    
def get_db():
    return getdb                  
    
db_dependency = Annotated[Session, Depends(get_db)] 

'''''
# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)
# method for start the MongoDb Connection
async def startup_db_client(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017/")
    app.mongodb = app.mongodb_client.get_database("hr_module")
    print("MongoDB connected.")

# method to close the database connection
async def shutdown_db_client(app: FastAPI):
    app.mongodb_client.close()
    print("Database disconnected.") 
'''
