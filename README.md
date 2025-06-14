## User Management (API) 

A lightweight, scalable REST API built with **FastAPI**, **MongoDB**, and **JWT authentication**.  
It includes full CRUD functionality for users, token-based authentication, and interactive Swagger docs. 

## Features  


- 🔐 **JWT Authentication** _Token-based access_
- 🧾 **Swagger UI** _for testing and documentation_
- 👤 **User CRUD Operations** _Create, Read, Update & Delete_
- 📦 **MongoDB Integration**
- ⚡ **FastAPI performance**
- 📁 Clean and modular project structure 

```python

## User Controller
@router.get('/all', response_model=List[User], dependencies=[Depends(verify_token)])
async def get_all(db = Depends(get_db)):
    list = await users_service.get_all(db)  
    return list
## User Service
async def get_all(db: AsyncIOMotorDatabase) -> List[dict]:
    try:
        users_cursor = db["users"].find({})
        users = await users_cursor.to_list()
        return users  
    except PyMongoError as e:
        raise  # Let the global handler catch this 
```
 
## Create virtual environment & install dependencies 


- `python -m venv venv`
- _`venv\Scripts\activate`_ <strong>_Windows_</strong>
- _`source venv/bin/activate`_ <strong>_macOS/Linux_</strong>
- `pip install -r requirements.txt`

## Clone the repository 

`git clone https://github.com/iamnomandra/user-management.git`

`cd user_management` 

## Run the server  

- `uvicorn main:app --reload` 

## Visit  
 
- [http://127.0.0.1:8000/api/gateway](http://127.0.0.1:8000/api/gateway) 🚀
  
- [http://127.0.0.1:8000/api/gateway/redocs](http://127.0.0.1:8000/api/gateway/redocs) 🚀

## Screenshot
- Custom swagger ui 
<img src="https://github.com/iamnomandra/user-management/blob/main/Screenshot%202025-06-15%20020841.png" width="800">  
 
<img src="https://github.com/iamnomandra/user-management/blob/main/Screenshot%202025-06-15%20020904.png" width="800">

- Overridden redoc
<img src="https://github.com/iamnomandra/user-management/blob/main/Screenshot%202025-06-15%20021558.png" width="800">  

<img src="https://github.com/iamnomandra/user-management/blob/main/Screenshot%202025-06-15%20021542.png" width="800">
  
## License 
 
 - MIT License
  
_`For the full README content, including setup instructions, advanced configurations, and contribution guidelines, <br>
visit the repository directly at [FastAPI](https://fastapi.tiangolo.com/).`_


