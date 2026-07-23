# ============================================================
# Standard Library
# ============================================================

from enum import Enum


# ============================================================
# Role Name Enum
# ============================================================

class RoleName(str, Enum):
    """
    System roles used throughout the application.
    """

    SUPER_ADMIN = "SUPER_ADMIN"

    PROPERTY_OWNER = "PROPERTY_OWNER"

    CUSTOMER = "CUSTOMER"