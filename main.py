from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt

class User(BaseModel):
    name: str
    email: str
    age: int


app = FastAPI()
print("✅ Running the CORRECT main.py")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 특정 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

def get_database():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["chat_database"]  # Replace with your database name
        return db
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    

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

#------------Member ---------------#
class LoginModel(BaseModel):
    username:str
    password:str
    
@app.post("/login")
def login_general(user: LoginModel, db=Depends(get_database)):
    print("start general login")

    # 데이터베이스에서 사용자 컬렉션 참조
    users_collection = db["usernames"]

    # 사용자 검색
    db_user = users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    # 비밀번호 검증
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Login successful", "username": user.username}

# 전체 회원조회 
@app.get("/members")
def getAllMembers(db=Depends(get_database)):
    users_collection = db["usernames"]
    members = list(users_collection.find({}, {"_id": 0}))  # Exclude MongoDB `_id`
    return JSONResponse(content=members, status_code=200)

# 회원가입 
@app.post("/signIN")
def signIn(user : LoginModel,db=Depends(get_database)):
    
    collections = db["usernames"]

    db_user = collections.find_one({"username": user.username})
    if db_user:
        raise HTTPException(status_code=401, detail="Already signed in")
    
    result = collections.insert_one(user.dict())
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to insert user")
    
    return {"message": "User inserted successfully", "user_id": str(result.inserted_id)}


# 구글 로그인 
GOOGLE_CLIENT_ID = "1007643601883-kf6s28beaotuv83d3bs61hkufomo73jc.apps.googleusercontent.com"

# 사용자 데이터 모델
class TokenModel(BaseModel):
    id_token: str

# Google 토큰 검증 함수
def verify_google_token(token: str):
    try:
        # Google의 ID 토큰 검증
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        return id_info  # 이메일, 이름 등 사용자 정보 반환
    except ValueError as e:
        logging.error(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid Google token")

@app.post("/login/google")
async def google_login(token_data: TokenModel):
    print("⏳ Login to Google ... ing")
    id_info = verify_google_token(token_data.id_token)
    return {
        "email": id_info["email"],
        "name": id_info.get("name", "Unknown"),
        "picture": id_info.get("picture", None),
        "message": "Google login successful"
    }
