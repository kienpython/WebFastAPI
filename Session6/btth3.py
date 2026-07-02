from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

app = FastAPI()


class RoomStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"


class Slot(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"


rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]


class RoomCreate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    status: RoomStatus


class RoomUpdate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    status: RoomStatus


class RoomBookingCreate(BaseModel):
    room_id: int
    class_name: str = Field(..., min_length=1)
    student_count: int = Field(..., gt=0)
    date: str
    slot: Slot


def find_room_by_id(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room
    return None


def is_duplicate_room_code(code: str, room_id: Optional[int] = None):
    for room in rooms:
        if room["code"].lower() == code.lower() and room["id"] != room_id:
            return True
    return False


def is_duplicate_booking(room_id: int, date: str, slot: str):
    for booking in room_bookings:
        if (
            booking["room_id"] == room_id
            and booking["date"] == date
            and booking["slot"] == slot
        ):
            return True
    return False


@app.post("/rooms", status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate):
    if is_duplicate_room_code(room.code):
        raise HTTPException(status_code=400, detail="Room code already exists")

    new_id = max(item["id"] for item in rooms) + 1

    new_room = {
        "id": new_id,
        "code": room.code,
        "name": room.name,
        "capacity": room.capacity,
        "status": room.status.value
    }

    rooms.append(new_room)

    return {
        "message": "Create room successfully",
        "data": new_room
    }


@app.get("/rooms")
def get_rooms(
    keyword: Optional[str] = None,
    status: Optional[RoomStatus] = None,
    min_capacity: Optional[int] = None
):
    result = rooms

    if keyword:
        keyword_lower = keyword.lower()
        result = [
            room for room in result
            if keyword_lower in room["code"].lower()
            or keyword_lower in room["name"].lower()
        ]

    if status is not None:
        result = [
            room for room in result
            if room["status"] == status.value
        ]

    if min_capacity is not None:
        result = [
            room for room in result
            if room["capacity"] >= min_capacity
        ]

    return {
        "message": "Get rooms successfully",
        "data": result
    }


@app.get("/rooms/{room_id}")
def get_room_detail(room_id: int):
    room = find_room_by_id(room_id)

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    return {
        "message": "Get room detail successfully",
        "data": room
    }


@app.put("/rooms/{room_id}")
def update_room(room_id: int, room_update: RoomUpdate):
    room = find_room_by_id(room_id)

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    if is_duplicate_room_code(room_update.code, room_id):
        raise HTTPException(status_code=400, detail="Room code already exists")

    room["code"] = room_update.code
    room["name"] = room_update.name
    room["capacity"] = room_update.capacity
    room["status"] = room_update.status.value

    return {
        "message": "Update room successfully",
        "data": room
    }


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    room = find_room_by_id(room_id)

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    rooms.remove(room)

    return {
        "message": "Delete room successfully"
    }


@app.post("/room-bookings", status_code=status.HTTP_201_CREATED)
def create_room_booking(booking: RoomBookingCreate):
    room = find_room_by_id(booking.room_id)

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    if room["status"] != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Room is not available")

    if booking.student_count > room["capacity"]:
        raise HTTPException(status_code=400, detail="Student count exceeds room capacity")

    if is_duplicate_booking(
        booking.room_id,
        booking.date,
        booking.slot.value
    ):
        raise HTTPException(status_code=400, detail="Room already booked at this date and slot")

    new_id = max(item["id"] for item in room_bookings) + 1

    new_booking = {
        "id": new_id,
        "room_id": booking.room_id,
        "class_name": booking.class_name,
        "student_count": booking.student_count,
        "date": booking.date,
        "slot": booking.slot.value
    }

    room_bookings.append(new_booking)

    return {
        "message": "Create room booking successfully",
        "data": new_booking
    }


@app.get("/room-bookings")
def get_room_bookings():
    return {
        "message": "Get room bookings successfully",
        "data": room_bookings
    }