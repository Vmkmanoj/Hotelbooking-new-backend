# ============================================================
# Third Party
# ============================================================

from pydantic import BaseModel


# ============================================================
# Generic API Responses
# ============================================================

class ApiResponse(BaseModel):
    """
    Generic API response.
    """

    success: bool
    message: str


class SuccessResponse(ApiResponse):
    """
    Generic success response.
    """

    pass