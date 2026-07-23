from enum import Enum


class RoomImageType(str, Enum):
    ROOM = "ROOM"
    BATHROOM = "BATHROOM"
    BALCONY = "BALCONY"
    VIEW = "VIEW"
    OTHER = "OTHER"