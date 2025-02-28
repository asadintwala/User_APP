from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from app.schemas.user_schema import User, UserUpdate, UserBase
from app.database import collection
from app.utils.utils import object_id_to_str, handle_db_error
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.utils.cache import get_cache, set_cache, delete_cache
from datetime import datetime

router = APIRouter(prefix='/v1')

# Fetch users with optional filtering and caching
@router.get("/users", response_model=List[User])
async def get_users(
    user_id: Optional[str] = None,
    limit: int = Query(10, ge=1, le=10),
    page: int = Query(1, ge=1),
    is_active: Optional[bool] = None,
    gender: Optional[str] = None
):
    try:
        skip = (page - 1) * limit
        query = {}
        if user_id:
            if not ObjectId.is_valid(user_id):
                return {"error": "Invalid User ID format."}  # Return instead of raise
            query["_id"] = ObjectId(user_id)
        if is_active is not None:
            query["is_active"] = is_active
        if gender:
            query["gender"] = gender
        
        total_users = collection.count_documents(query)
        users_cursor = collection.find(query).skip(skip).limit(limit)
        users = [object_id_to_str(user) for user in users_cursor]
        return users  # Removed cache for instant reflection
    except PyMongoError as e:
        return {"error": str(e)}  # Return instead of raise

# Fetch user history including last updates
@router.get("/user_history/{user_id}", response_model=Dict[str, Any])
async def get_user_history(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            return {"error": "Invalid User ID format."}  # Return instead of raise
        user = collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"error": "User not found."}  # Return instead of raise
        return {"user": object_id_to_str(user), "last_updates": user.get("updates", [])[-5:], "message": "Last updates of the user."}
    except PyMongoError as e:
        return {"error": str(e)}  # Return instead of raise

# Create a new user
@router.post("/users", response_model=Dict[str, Any])
async def create_user(user: UserBase):
    try:
        existing_user = collection.find_one({'email': user.email})
        if existing_user:
            return {"error": "Email already registered."}  # Return instead of raise
        new_user = user.model_dump()
        result = collection.insert_one(new_user)
        created_user = object_id_to_str(collection.find_one({"_id": result.inserted_id}))
        return {"user": created_user, "message": "New user created successfully."}
    except PyMongoError as e:
        return {"error": str(e)}  # Return instead of raise

# Fully update user details
@router.put("/users/{user_id}", response_model=Dict[str, Any])
async def update_user_full(user_id: str, user: UserBase):
    try:
        if not ObjectId.is_valid(user_id):
            return {"error": "Invalid User ID format."}  # Return instead of raise
        existing_user = collection.find_one({'_id': ObjectId(user_id)})
        if not existing_user:
            return {"error": "User not found."}  # Return instead of raise
        update_data = user.model_dump()
        update_entry = {"updated_at": datetime.utcnow(), "updated_data": update_data}
        collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data, '$push': {'updates': {'$each': [update_entry], '$slice': -5}}})
        updated_user = collection.find_one({'_id': ObjectId(user_id)})
        return {"user": object_id_to_str(updated_user), "message": "Full user update done successfully."}
    except PyMongoError as e:
        return {"error": str(e)}  # Return instead of raise

# Partially update user details
@router.patch("/users/{user_id}", response_model=Dict[str, Any])
async def update_user_partial(user_id: str, user: UserUpdate):
    try:
        if not ObjectId.is_valid(user_id):
            return {"error": "Invalid User ID format."}  # Return instead of raise
        existing_user = collection.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            return {"error": "User not found."}  # Return instead of raise
        update_data = {key: value for key, value in user.model_dump(exclude_unset=True).items()}
        if not update_data:
            return {"error": "No valid fields provided for update."}  # Return instead of raise
        update_entry = {"updated_at": datetime.utcnow(), "updated_data": update_data}
        collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data, "$push": {"updates": {"$each": [update_entry], "$slice": -5}}})
        updated_user = collection.find_one({"_id": ObjectId(user_id)})
        return {"user": object_id_to_str(updated_user), "message": "User partially updated successfully."}
    except PyMongoError as e:
        return {"error": str(e)}  # Return instead of raise

# Delete a user
@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            return {"error": "Invalid User ID format."}  # Return instead of raise
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            return {"message": "User deleted successfully"}
        return {"error": "User not found"}  # Return instead of raise
    except PyMongoError as e:
        return {"error": str(e)}  # Return instead of raise
