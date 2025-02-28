from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.mongo_url)
# userDB Database connections
user_db = client[settings.db_name]
collection = user_db[settings.collection_name]