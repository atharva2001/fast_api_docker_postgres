from fastapi import APIRouter, Request 
from log_util import get_logger
from pydantic import BaseModel
from database import items
import json

# Create a router object
router = APIRouter(
    prefix="/items",
    tags=["items"],
)

logging = get_logger("items_route.log", "ItemsLogger")

@router.get("/get_item/{id}")
async def get_item(request: Request, id: str):
    logging.info(f"GET request to get item with id: {id}")
    cache = request.app.state.redis_client.get(f"item_{id}")
    if cache:
        logging.info(f"Cache hit for item {id}")
        return json.loads(cache)
    else:
        logging.info(f"Cache miss for item {id}")
        cursor = request.app.state.db.cursor()
        data = (id,)
        response = await items.get_item(cursor, data)
        if "error" in response:
            return response
        res_tup = list(response["response"][:-1])
        res_tup.append(str(response["response"][3]))
        response = {
            "response": res_tup,
        }

        logging.info(f"Setting cache for item {id}")
        request.app.state.redis_client.set(f"item_{id}", json.dumps(response))
        return response

@router.get("/get_all")
async def get_all(request: Request):
    logging.info("Fetching all the data")
    cache = request.app.state.redis_client.get(f"get_items")
    if cache:
        logging.info("Cache hit for all items")
        return json.loads(cache)
    else:
        logging.info("Cache miss for all items")
        cursor = request.app.state.db.cursor()
        response = await items.get_all(cursor)
        if "error" in response:
            return response
        final_res = []
        for res in response["response"]:
            res_tup = list(res[:-1])
            res_tup.append(str(res[3]))
            final_res.append(res_tup)
        response = {
            "response": final_res,
        }
        request.app.state.redis_client.set(f"get_items", json.dumps(response))
        return {"response": response["response"]}
    

class ItemBody(BaseModel):
    category: str
    name: str
    price: int

@router.post("/create_item")
async def create_item(request: Request, data: ItemBody):
    cursor = request.app.state.db.cursor()
    request.app.state.redis_client.delete(f"get_items")
    return await items.create_item(cursor, data, request)

@router.delete("/delete_item/{id}")
async def delete_item(request: Request, id: str):
    logging.info(f"Deleting item with id: {id}")
    resp = await items.get_item(request.app.state.db.cursor(), (id,))
    if "error" in resp:
        return {"error": "Item not found"}
    cursor = request.app.state.db.cursor()
    data = (id,)
    response = await items.delete_item(cursor, data, request)
    request.app.state.redis_client.delete(f"item_{id}")
    request.app.state.redis_client.delete(f"get_items")
    if response:
        return {"reponse": "Successfully deleted the item"}
    else:
        return {"response": "Item not found"}   