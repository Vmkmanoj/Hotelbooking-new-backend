# ============================================================
# Standard Library
# ============================================================

from enum import Enum


# ============================================================
# Property Type Enum
# ============================================================

class PropertyType(str, Enum):
    """
    Represents the type of property listed on the platform.
    """

    HOTEL = "HOTEL"

    APARTMENT = "APARTMENT"

    VILLA = "VILLA"

    RESORT = "RESORT"

    HOSTEL = "HOSTEL"

    HOMESTAY = "HOMESTAY"