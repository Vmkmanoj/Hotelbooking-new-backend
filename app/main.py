# ============================================================
# Third Party
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# Local Imports
# ============================================================

from app.api.router import api_router
from app.core.config import settings

# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# ============================================================
# CORS Configuration
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# API Router
# ============================================================

app.include_router(
    api_router,
    prefix="/api/v1",
)

# ============================================================
# Health Check
# ============================================================

@app.get(
    "/",
    tags=["Health"],
)
async def health_check():

    return {
        "message": "Hotel Booking Backend is running."
    }