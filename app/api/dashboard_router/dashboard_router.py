# ============================================================
# Third Party
# ============================================================

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

# ============================================================
# Local Imports
# ============================================================

from app.database.session import get_db

from app.schema.dashboard_schema.dashboardSchema import (
    DashboardResponse,
)

from app.services.dashboard_services.dashboard_service import (
    DashboardService,
)

# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/super-admin-dashboard/dashboard",
    tags=["Dashboard"],
)

# ============================================================
# Service Dependency
# ============================================================

def get_dashboard_service(
    db: AsyncSession = Depends(get_db),
) -> DashboardService:
    return DashboardService(db)

# ============================================================
# Get Dashboard
# ============================================================

@router.get(
    "",
    response_model=DashboardResponse,
    status_code=status.HTTP_200_OK,
)
async def get_dashboard(
    service: DashboardService = Depends(
        get_dashboard_service,
    ),
) -> DashboardResponse:
    """
    Retrieve dashboard statistics.
    """

    return await service.get_dashboard()