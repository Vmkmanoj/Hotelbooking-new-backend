# ============================================================
# Third Party
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# Local Imports
# ============================================================

from contextlib import asynccontextmanager
from app.api.router import api_router
from app.core.config import settings
from app.database import AsyncSessionLocal
from app.seed.seed_data import seed_database

# ============================================================
# FastAPI Application
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await seed_database(db)
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
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