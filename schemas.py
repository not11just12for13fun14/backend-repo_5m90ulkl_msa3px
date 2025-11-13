"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Interest(BaseModel):
    """
    Youth interest sign-ups
    Collection name: "interest"
    """
    full_name: str = Field(..., min_length=2, description="Full name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone number")
    age: Optional[int] = Field(None, ge=10, le=30, description="Age (optional)")
    preferred_ministry: Optional[str] = Field(None, description="Area you'd like to serve or join")
    message: Optional[str] = Field(None, max_length=1000, description="Tell us a bit about you")

class MediaItem(BaseModel):
    """
    Photos/videos for the gallery
    Collection name: "mediaitem" (use "mediaitem" or query as "mediaitem")
    """
    kind: str = Field(..., description="photo or video")
    url: HttpUrl = Field(..., description="Direct image URL or video URL (YouTube/Vimeo)")
    caption: Optional[str] = Field(None, max_length=200)
    taken_at: Optional[str] = Field(None, description="Date string, e.g., 2024-09-12")

class EventEntry(BaseModel):
    """
    Events that youth members joined
    Collection name: "evententry"
    """
    title: str = Field(..., description="Event title")
    date: str = Field(..., description="Date string, e.g., 2024-06-21")
    location: Optional[str] = Field(None, description="Where it took place")
    description: Optional[str] = Field(None, description="Short summary")
    photos: Optional[List[HttpUrl]] = Field(default=None, description="Optional list of photo URLs")
    video: Optional[HttpUrl] = Field(default=None, description="Optional video URL (YouTube/Vimeo)")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
