from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from pymongo import MongoClient

from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int


app = FastAPI()
print("✅ Running the CORRECT main.py")


# Optionally add a middleware to log requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn.access")
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

data = [
    
    
{
        "title": "Today's News2",
        "newsItems": [
            {"title": "Breaking News 1", "imageUrl": "https://cdn.travie.com/news/photo/first/201710/img_19975_1.jpg"},
            {"title": "Breaking News 2", "imageUrl": "https://example.com/news2.jpg"}
        ]
    },

]


# Replace with your direct connection string
MONGO_URI = "mongodb+srv://waterbang12:happy4216@cluster0.5uuwv.mongodb.net/?retryWrites=true&w=majority"

try:
    print("⏳ Attempting to connect to MongoDB...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["chat_database"]
    users_collection = db["users"]
    client.admin.command("ping")
    print("✅ MongoDB connection successful!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.post("/users", status_code=201)
def create_user(user: User):
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    users_collection.insert_one(user.dict())
    return {"message": "User created successfully"}
@app.get("/users")
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return {"users": users}
@app.get("/news")

@app.get("/news", status_code=200)
def get_news():
    news_list = list(users_collection.find({}, {"_id": 0}))  # Exclude MongoDB `_id`
    return JSONResponse(content=news_list, status_code=200)
@app.post("/news", status_code=201)
def create_news():
    print("✅ MongoDB connection successful!")
    
    users_collection.insert_many(data)
    return {"message": "User created successfully"}





@app.get("/dummy")


def get_users():
    print("🔹 /dummy route was triggered!")
    inserted_ids = users_collection.insert_many(data).inserted_ids
    
    return {"message": "News created successfully", "inserted_ids": [str(i) for i in inserted_ids]}

    
