from .room_router import router as room_router
from .room_type_router import router as room_type_router
from .room_image_router import router as room_image_router
from .room_amenity_router import router as room_amenity_router

__all__ = [
    "room_router",
    "room_type_router",
    "room_image_router",
    "room_amenity_router",
]