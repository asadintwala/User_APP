# user_schema is for API Request/Response Validation
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from fastapi import APIRouter

router = APIRouter()

# Base schema for User
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description='Name must be within 2-50 characters.')
    email: EmailStr
    age: int = Field(..., ge=18, le=60, description='Age must be between 18 and 60.')
    gender: Literal['Male', 'Female', 'Non Binary'] # Literal to restrict a field to a fixed set of values 
    country: str = Field(..., min_length = 2, max_length = 50, description = 'Country must be valid string between 2-50 characters.' )
    is_active: bool = Field(..., description = 'Must be true or false.')

# Schema for patching field/s for an existing user   
class UserCreate(UserBase):
    pass  

# Schema for returning user data, including MongoDB _id in str to show in json formate in FastAPI
class User(UserBase):
    id: str = Field(..., alias="_id") # Mapped MongoDB '_id' to 'id' in response

    class Config:
        populate_by_name = True  # Ensures '_id' from MongoDB is maped as 'id' in response

# Update schema for PATCH API
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, description = 'Name must be between 2-50 characters.')
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=18, le=60, description = 'Age must be between 18-70.')
    gender: Optional[Literal['Male', 'Female', 'Non Binary']] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None