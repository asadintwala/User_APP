# user-model is for MondoDb data structue
from pydantic import BaseModel, EmailStr
from typing import Optional

# User model representing MongoDB document structure
class UserModel(BaseModel):
    id: Optional[str]  # MongoDB _id stored as string
    name: str  # User's name
    email: EmailStr  # Email id in valid email format
    age: int  # User's age
    gender: str  # Gender information
    country: str  # Country of the user
    is_active: bool  # Status flag
