from datetime import date
from pydantic import BaseModel, Field, EmailStr

#User Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

    class Config:
        from_attributes=True

#Room Schemas
class RoomCreate(BaseModel):
    hotel_name: str
    room_type: str
    location: str
    price: float= Field(gt=0)
    capacity: int= Field(gt=0)

class RoomResponse(BaseModel):
    id: str
    owner_id: str
    hotel_name: str
    room_type: str
    location: str
    price: float
    capacity: int

    class Config:
        from_attributes=True

#Booking Schemas
class BookingCreate(BaseModel):
    room_id:str
    check_in:date
    check_out:date

class BookingResponse(BaseModel):
    id: str
    user_id: str
    room_id: str
    check_in: date
    check_out: date
    status: str

    class Config:
        from_attributes=True