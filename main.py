from uuid import uuid4

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

from database import  Base, engine, SessionLocal
from models import User, Room, Booking
from schemas import UserCreate,UserResponse,UserLogin, RoomCreate,RoomResponse,BookingCreate,BookingResponse
from auth import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Hotel Booking Platform API")

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return{"message": " Hotel Booking API is running"}

@app.post("/register",response_model=UserResponse,status_code=201)
def register(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    new_user=User(
       id=str(uuid4()),
       name=user.name,
       email=user.email,
       password=hash_password(user.password)
   ) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == form_data.username).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=401,detail="Invalid email or password")

    access_token = create_access_token(existing_user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me")
def get_my_profile(user_id:str=Depends(get_current_user)):
    return {"message":"Authentication successful",
            "user_id": user_id}

@app.post("/rooms", response_model=RoomResponse, status_code=201)
def create_room(room: RoomCreate,user_id: str = Depends(get_current_user),db: Session = Depends(get_db)):
    new_room = Room(
        id=str(uuid4()),
        owner_id=user_id,
        hotel_name=room.hotel_name,
        room_type=room.room_type,
        location=room.location,
        price=room.price,
        capacity=room.capacity
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room

@app.get("/rooms", response_model=list[RoomResponse])
def get_rooms(
    db: Session = Depends(get_db)
):
    rooms = db.query(Room).all()

    return rooms

@app.put("/rooms/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: str,
    room: RoomCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not existing_room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    # Check ownership
    if existing_room.owner_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own room"
        )

    existing_room.hotel_name = room.hotel_name
    existing_room.room_type = room.room_type
    existing_room.location = room.location
    existing_room.price = room.price
    existing_room.capacity = room.capacity

    db.commit()
    db.refresh(existing_room)

    return existing_room

@app.delete("/rooms/{room_id}")
def delete_room(
    room_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not existing_room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    # Check ownership
    if existing_room.owner_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own room"
        )

    db.delete(existing_room)
    db.commit()

    return {
        "message": "Room deleted successfully"
    }

@app.post(
    "/bookings",
    response_model=BookingResponse,
    status_code=201
)
def create_booking(
    booking: BookingCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check that check-in is before check-out
    if booking.check_in >= booking.check_out:
        raise HTTPException(
            status_code=400,
            detail="Check-out date must be after check-in date"
        )

    # Check that the room exists
    room = db.query(Room).filter(
        Room.id == booking.room_id
    ).first()

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    # Check for overlapping bookings
    overlapping_booking = db.query(Booking).filter(
        Booking.room_id == booking.room_id,
        Booking.status == "confirmed",
        Booking.check_in < booking.check_out,
        Booking.check_out > booking.check_in
    ).first()

    if overlapping_booking:
        raise HTTPException(
            status_code=400,
            detail="Room is already booked for these dates"
        )

    # Create booking
    new_booking = Booking(
        id=str(uuid4()),
        room_id=booking.room_id,
        user_id=user_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        status="confirmed"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

@app.get("/bookings", response_model=list[BookingResponse])
def get_my_bookings(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == user_id
    ).all()

    return bookings

@app.get("/rooms/search", response_model=list[RoomResponse])
def search_rooms(
    location: str | None = None,
    room_type: str | None = None,
    capacity: int | None = None,
    check_in: datetime | None = None,
    check_out: datetime | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Room)

    if location:
        query = query.filter(Room.location == location)

    if room_type:
        query = query.filter(Room.room_type == room_type)

    if capacity:
        query = query.filter(Room.capacity >= capacity)

    if check_in and check_out:

        if check_in >= check_out:
            raise HTTPException(
                status_code=400,
                detail="Check-out date must be after check-in date"
            )

        booked_room_ids = db.query(Booking.room_id).filter(
            Booking.status == "confirmed",
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).subquery()

        query = query.filter(
            ~Room.id.in_(booked_room_ids)
        )

    return query.all()