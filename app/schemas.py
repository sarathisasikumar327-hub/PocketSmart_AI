from typing import Optional
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: str
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=100000000)
    room: str = "Living Room"
    style: str = "Modern"
    lights: int = Field(default=2, ge=0, le=50)
    fans: int = Field(default=1, ge=0, le=20)
    tables: int = Field(default=1, ge=0, le=20)
    extra: Optional[str] = ""

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=100000000)
    event_type: str = "Birthday"
    guests: int = Field(gt=0, le=100000)
    venue: str = "Indoor"
    food_preference: str = "Mixed"
    extra: Optional[str] = ""

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=100000000)
    occasion: str = "Wedding"
    style: str = "Elegant"
    metal: str = "Any"
    outfit_color: Optional[str] = ""
    extra: Optional[str] = ""
