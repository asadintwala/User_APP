from fastapi import HTTPException
import aioredis
import json
from app.database import collection

# Convert MongoDB ObjectId to string
def object_id_to_str(document):
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    return document

# Handle MongoDB errors
def handle_db_error(error):
    raise HTTPException(status_code=500, detail=str(error))

REDIS_STREAM = 'user_update_stream'
# This function will generate event and will push them in Redis Stream
async def publish_update_event(user_id: str, update_data: dict):
    redis = await aioredis.from_url("redis://localhost")
    event = {"user_id": user_id, "update_data": update_data}
    await redis.xadd(REDIS_STREAM, event)
    await redis.close()

async def consume_updated_events():
    redis = await aioredis.from_url("redis://localhost")

    while True:
        events = await redis.xread({REDIS_STREAM: "0"}, count=5, block=5000)
        for stream, messages in events:
            for msg_id, event in messages:
                user_id = event[b"user_id"].decode()
                update_data = json.loads(event[b"update_data"].decode())

                # MongoDB me update history store karna
                collection.update_one(
                    {"_id": user_id},
                    {"$push": {"updates": {"$each": [update_data], "$slice": -5}}}
                )

    await redis.close()