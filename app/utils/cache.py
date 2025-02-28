import redis
import json

# Redis Client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Function to get cache data
def get_cache(key):
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

# Function to set cache data
def set_cache(key, value, expiry=60):  # Cache expiry = 60 seconds
    redis_client.set(key, json.dumps(value), ex=expiry)

# Function to delete cache
def delete_cache(key):
    redis_client.delete(key)
