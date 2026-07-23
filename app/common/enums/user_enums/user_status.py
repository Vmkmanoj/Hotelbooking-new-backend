# ============================================================
# Standard Library
# ============================================================

from enum import Enum


class UserStatus(str, Enum):
    """
    Represents the lifecycle status
    of a user account.
    """

    ACTIVE = "ACTIVE"

    SUSPENDED = "SUSPENDED"

    DEACTIVATED = "DEACTIVATED"