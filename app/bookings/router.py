from fastapi import APIRouter, Request
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking

router = APIRouter(
    prefix="/bookings",
    tags=['Bookings'],
)


@router.get("")
async def get_bookings(request: Request): # -> list[SBooking]:
    print(request.cookies)
    #return await BookingDAO.find_all()