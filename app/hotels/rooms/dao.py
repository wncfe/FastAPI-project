from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels
    
    