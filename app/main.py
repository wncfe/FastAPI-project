from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


class HotelSearchArgs():
    def __init__(
        self,
        location: str,
        date_in: date,
        date_out: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = Query(None, ge=1, le=5),
    ):
        self.location = location
        self.date_in = date_in
        self.date_out = date_out
        self.has_spa = has_spa
        self.stars = stars

@app.get('/hotels')
def get_hotels(
    search_args: HotelSearchArgs = Depends()
):
    hotels = [
        {
            'adress': 'Улица Макарова, 2, Москва',
            'name': 'Super Star',
            'stars': 5,
        },
    ]
    return search_args


class SBooking(BaseModel):
    hotel_id: int
    date_in: date
    date_out: date

@app.post('/bookings')
def add_booking(booking: SBooking):
    pass
    