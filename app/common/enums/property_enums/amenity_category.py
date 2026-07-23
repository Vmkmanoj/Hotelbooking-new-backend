# ============================================================
# Standard Library
# ============================================================

from enum import Enum

# ============================================================
# Amenity Category Enum
# ============================================================

class AmenityCategory(str, Enum):
    """
    Master categories for amenities used across
    Properties and Room Types.
    """

    # ========================================================
    # Property Amenities
    # ========================================================

    GENERAL = "GENERAL"

    FOOD_AND_BEVERAGE = "FOOD_AND_BEVERAGE"

    WELLNESS = "WELLNESS"

    RECREATION = "RECREATION"

    BUSINESS = "BUSINESS"

    TRANSPORT = "TRANSPORT"

    ACCESSIBILITY = "ACCESSIBILITY"

    SAFETY_AND_SECURITY = "SAFETY_AND_SECURITY"

    FAMILY = "FAMILY"

    OUTDOOR = "OUTDOOR"

    PET_FRIENDLY = "PET_FRIENDLY"

    SERVICES = "SERVICES"

    # ========================================================
    # Room Amenities
    # ========================================================

    BEDROOM = "BEDROOM"

    BATHROOM = "BATHROOM"

    ENTERTAINMENT = "ENTERTAINMENT"

    COMFORT = "COMFORT"

    KITCHEN = "KITCHEN"

    CONNECTIVITY = "CONNECTIVITY"

    VIEW = "VIEW"