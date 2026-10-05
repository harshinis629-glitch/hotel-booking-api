from database import Base
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey

class User(Base):
    __tablename__="users"

    id=Column(String(36),primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    email=Column(String(100),nullable=False,unique=True,index=True)
    password=Column(String(255),nullable=False)

class Room(Base):
    __tablename__="rooms"

    id=Column(String(36),primary_key=True,index=True)
    owner_id=Column(String(36),ForeignKey("users.id"),nullable=False)

    hotel_name=Column(String(150),nullable=False)
    room_type=Column(String(100),nullable=False)
    location=Column(String(150),nullable=False)

    price=Column(Float,nullable=False)
    capacity=Column(Integer,nullable=False)

class Booking(Base):
    __tablename__="bookings"

    id=Column(String(36),primary_key=True,index=True)
    user_id=Column(String(36),ForeignKey("users.id"),nullable=False)
    room_id=Column(String(36),ForeignKey("rooms.id"),nullable=False)

    check_in=Column(DateTime,nullable=False)
    check_out=Column(DateTime,nullable=False)

    status=Column(String(20),nullable=False,default="confirmed")
    