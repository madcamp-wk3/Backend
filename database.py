
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in the .env file!")

# MongoDB 클라이언트 연결
client = MongoClient(MONGO_URI)
db = client["chat_database"]  # 사용할 데이터베이스 이름
