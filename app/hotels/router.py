from fastapi import APIRouter
from datetime import date
from app.hotels.dao import HotelsDAO
from typing import Optional

router = APIRouter(
    prefix="/hotels",
    tags=['Hotels'],
    )


@router.get('/{location}')
async def get_hotels(
    location: str, 
    date_from: Optional[date] = None, 
    date_to: Optional[date] = None
    ):
    
    return await HotelsDAO.find_hotels_by_location(location, date_from, date_to)
    