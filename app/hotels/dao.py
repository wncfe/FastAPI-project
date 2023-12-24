from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from sqlalchemy import select, literal, and_, or_, func, distinct, label
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings

class HotelsDAO(BaseDAO):
    model = Hotels
    
    
    @classmethod
    async def find_hotels_by_location(cls, location, date_from, date_to):
        async with async_session_maker() as session:
            
            relevant_hotels = select(Hotels).filter(
                    Hotels.location.like(f'%{location}%')
                ).cte('relevant_hotels')
            
            hotel_rooms = select(label('room_id', Rooms.id), label('hotel_id', relevant_hotels.c.id)).join(
                relevant_hotels, relevant_hotels.c.id == Rooms.hotel_id, isouter=True
            ).where(
                Rooms.hotel_id == relevant_hotels.c.id
            ).cte('hotel_rooms')
            
            
            booked_rooms = select(hotel_rooms.c.hotel_id, func.count(Bookings.room_id)).join(
                hotel_rooms, isouter=True,
                ).where(
                    and_(
                        hotel_rooms.c.room_id == Bookings.room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from
                            )
                        )
                    )
                ).group_by(hotel_rooms.c.hotel_id).cte('booked_rooms')
                
            get_relevant_hotels = select(
                relevant_hotels,
                func.coalesce(relevant_hotels.c.rooms_quantity - booked_rooms.c.count, relevant_hotels.c.rooms_quantity).label('rooms_left')
                ).select_from(
                    relevant_hotels.outerjoin(booked_rooms, relevant_hotels.c.id == booked_rooms.c.hotel_id)
                ).where(func.coalesce(relevant_hotels.c.rooms_quantity - booked_rooms.c.count, relevant_hotels.c.rooms_quantity) > 0)
                
            result = await session.execute(get_relevant_hotels)
            
            return result.mappings().all()
        
        