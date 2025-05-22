from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
from route.users import router as users_router
from route.items import router as items_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from log_util import get_logger
from contextlib import asynccontextmanager
from database.core import connect_to_db
import redis 

limiter = Limiter(key_func=get_remote_address, default_limits=["1/second"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = connect_to_db()
    app.state.redis_client = redis.Redis(host="0.0.0.0", port=6379, db=0)
    logging.info(f"Connected to db: {app.state.db}")
    yield
    logging.info("Connection Close")
    app.state.db.close()


app = FastAPI(title="Router Example", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(users_router)
app.include_router(items_router)
app.add_middleware(SlowAPIMiddleware)

# Setup logger

logging = get_logger("app.log", "AppLogger")



@app.get("/")
async def root():
    logging.info("Root endpoint accessed")
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )