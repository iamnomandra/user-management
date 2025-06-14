
from config.settings import Settings 
settings = Settings()
 
DESC = f""" **{settings.APP_NAME} API** gives you awesome experience for CRUD operations 
with help of SQL Server. 

Developed By: Amit Kumar **(Full Stack Developer)**
Powered By:  **iamnomandra**
"""
TAGS_META = [  
    {
        "name": "Tokens",
        "description": "Access tokens for authorization of **API** to restrict unauthorize access.", 
    },
    {
        "name": "Users",
        "description": "Operations with users. The **CRUD** logic access from here.",
    }
]