# ============================================================
# Local Imports
# ============================================================

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dashboard_repositories.DashboardRepository import (
    DashboardRepository,
)

from app.schema.dashboard_schema.dashboardSchema import (
    DashboardResponse,
)

# ============================================================
# Dashboard Service
# ============================================================

class DashboardService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.repo = DashboardRepository(
            db,
        )

    # ========================================================
    # Get Dashboard Statistics
    # ========================================================

    async def get_dashboard(
        self,
    ) -> DashboardResponse:

        return DashboardResponse(
            total_users=await self.repo.total_users(),
            total_customers=await self.repo.total_customers(),
            total_property_owners=await self.repo.total_property_owners(),
            total_admins=await self.repo.total_admins(),
            total_properties=await self.repo.total_properties(),
            pending_properties=await self.repo.pending_properties(),
            approved_properties=await self.repo.approved_properties(),
            rejected_properties=await self.repo.rejected_properties(),
            suspended_properties=0,
        )