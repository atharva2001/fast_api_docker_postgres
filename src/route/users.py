'''
User's Router to route the api from `/users`. Some simple api calls, basic logic.
'''

from fastapi import APIRouter, Depends, Request
from log_util import get_logger
from pydantic import BaseModel
from database import users
import json

# Create a router object
router = APIRouter(
    prefix="/users",
    tags=["users"],
)


logging = get_logger("user_route.log", "UserLogger")


# Simple GET request to get all users
@router.get("/get_user/{id}")
async def get_user(request: Request, id: str):
    logging.info(f"GET request to get user with id: {id}")
    cache = request.app.state.redis_client.get(f"user_{id}")
    if cache:
        logging.info(f"Cache hit for user {id}")
        return json.loads(cache)
    else:
        logging.info(f"Cache miss for user {id}")
        cursor = request.app.state.db.cursor()
        data = (id,)
        response = await users.get_user(cursor, data)
        if "error" in response:
            return {"error": "User not found"}   
        
        res_tup = list(response["response"][:-1])
        res_tup.append(str(response["response"][4]))
        response = {
            "response": res_tup,
        }

        logging.info(f"Setting cache for user {id}")
        request.app.state.redis_client.set(f"user_{id}", json.dumps(response))
        return response 
        

@router.get("/get_all")
async def get_all(request: Request):
    logging.info("Fetching all the data")
    cache = request.app.state.redis_client.get(f"get_users")
    if cache:
        logging.info("Cache hit for all users")
        return json.loads(cache)
    else:
        logging.info("Cache miss for all users")
        cursor = request.app.state.db.cursor()
        response = await users.get_all(cursor)
        final_res = []
        if "error" in response:
            return response

        for res in response["response"]:
            res_tup = list(res[:-1])
            res_tup.append(str(res[4]))
            final_res.append(res_tup)
        response = {
            "response": final_res,
        }
        logging.info("Setting cache for all users")
        request.app.state.redis_client.set(f"get_users", json.dumps(response))
        return {"response": response["response"]}
    
    
class UserBody(BaseModel):
    name: str
    email: str
    age: int

@router.post("/create_user")
async def create_user(request: Request, data: UserBody):
    logging.info("Inserting the data")
    request.app.state.redis_client.delete(f"get_users")
    cursor = request.app.state.db.cursor()

    return await users.create_user(cursor, data, request)


@router.delete("/delete_user/{id}")
async def delete_user(request: Request, id: str):
    logging.info(f"Deleting the user with id: {id}")
    resp = await users.get_user(request.app.state.db.cursor(), (id,))
    if "error" in resp:
        return {"response": "User not found"}
    
    cursor = request.app.state.db.cursor()
    data = (id,)
    response = await users.delete_user(cursor, data, request)
    request.app.state.redis_client.delete(f"user_{id}")
    request.app.state.redis_client.delete(f"get_users")
   
    if response:
        return {"reponse": "Successfully deleted the user"}
    else:
        return {"response": "User not found"}    

