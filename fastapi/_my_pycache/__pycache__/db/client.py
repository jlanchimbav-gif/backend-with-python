from pymongo import MongoClient

# MongoDB connection
db_client = MongoClient("mongodb://localhost:27017/")
db = db_client["fastapi_db"]
users_collection = db["users"]
