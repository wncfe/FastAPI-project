from fastapi import APIRouter, Request, Depends
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependences import get_current_user


router = APIRouter(
    prefix="/bookings",
    tags=['Bookings'],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)): # -> list[SBooking]:
    return await BookingDAO.find_all(user_id=1)