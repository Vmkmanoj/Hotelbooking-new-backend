# ============================================================
# Third Party
# ============================================================

from fastapi import APIRouter

# ============================================================
# Local Imports
# ============================================================

from app.api.auth_router.auth_router import (
    router as auth_router,
)

from app.api.booking_router.booking_router import (
    router as booking_router,
)

from app.api.payment_router.payment_router import (
    router as payment_router,
)

from app.api.favorite_router.favorite_router import (
    router as favorite_router,
)

from app.api.dashboard_router.dashboard_router import (
    router as dashboard_router,
)

from app.api.super_admin_router.super_admin_router import (
    router as super_admin_router,
)

from app.api.property_router.property.property_router import (
    router as property_router,
)

from app.api.property_router.address.address_router import (
    router as address_router,
)

from app.api.property_router.amenities.amenities_router import (
    router as amenity_router,
)

from app.api.property_router.propertyimages.property_images_router import (
    router as property_image_router,
)

from app.api.property_router.propertyamenities.propertyamenities_router import (
    router as property_amenity_router,
)

from app.api.rooms_router.room_type_router import (
    router as room_type_router,
)

from app.api.rooms_router.room_router import (
    router as room_router,
)

from app.api.rooms_router.room_image_router import (
    router as room_image_router,
)

from app.api.rooms_router.room_amenity_router import (
    router as room_amenity_router,
)

# ============================================================
# Main API Router
# ============================================================

api_router = APIRouter()

# ============================================================
# Authentication
# ============================================================

api_router.include_router(auth_router)

# ============================================================
# Property Module
# ============================================================

api_router.include_router(property_router)
api_router.include_router(address_router)
api_router.include_router(amenity_router)
api_router.include_router(property_image_router)
api_router.include_router(property_amenity_router)

# ============================================================
# Room Module
# ============================================================

api_router.include_router(room_type_router)
api_router.include_router(room_router)
api_router.include_router(room_image_router)
api_router.include_router(room_amenity_router)

# ============================================================
# Booking Module
# ============================================================

api_router.include_router(booking_router)

# ============================================================
# Payment Module
# ============================================================

api_router.include_router(payment_router)

# ============================================================
# Favorites
# ============================================================

api_router.include_router(favorite_router)

# ============================================================
# Dashboard
# ============================================================

api_router.include_router(dashboard_router)

# ============================================================
# Super Admin
# ============================================================

api_router.include_router(super_admin_router)