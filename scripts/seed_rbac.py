# ============================================================
# Standard Library
# ============================================================

import asyncio

# ============================================================
# Third Party
# ============================================================

from sqlalchemy import select

# ============================================================
# Local Imports
# ============================================================

from app.core.password import hash_password
from app.database import AsyncSessionLocal

from app.modules.users.models import (
    Role,
    User,
)

from app.modules.auth.auth_constants import (
    SUPER_ADMIN,
    PROPERTY_OWNER,
    CUSTOMER,
)
from app.common.enums.user_enums.user_status import UserStatus


# ============================================================
# Seed RBAC
# ============================================================

async def seed_roles() -> None:
    """
    Seed default roles and Super Admin.
    Safe to execute multiple times.
    """

    async with AsyncSessionLocal() as db:

        # ----------------------------------------------------
        # Roles
        # ----------------------------------------------------

        role_names = [
            SUPER_ADMIN,
            PROPERTY_OWNER,
            CUSTOMER,
        ]

        role_map: dict[str, Role] = {}

        for role_name in role_names:

            result = await db.execute(
                select(Role).where(
                    Role.name == role_name
                )
            )

            role = result.scalar_one_or_none()

            if role is None:

                role = Role(
                    name=role_name,
                    description=f"{role_name} Role",
                    is_active=True,
                )

                db.add(role)

                await db.flush()

                print(f"✔ Created Role : {role_name}")

            else:

                print(f"✔ Role Exists  : {role_name}")

            role_map[role_name] = role

        # ----------------------------------------------------
        # Super Admin
        # ----------------------------------------------------

        admin_email = "admin@hotel.com"

        result = await db.execute(
            select(User).where(
                User.email == admin_email
            )
        )

        admin = result.scalar_one_or_none()

        if admin is None:

            admin = User(
                first_name="Super",
                last_name="Admin",
                email=admin_email,
                password_hash=hash_password("Admin@123"),
                role_id=role_map[SUPER_ADMIN].id,
                user_status=UserStatus.ACTIVE,
            )

            db.add(admin)

            print("✔ Super Admin Created")

        else:

            print("✔ Super Admin Already Exists")

        await db.commit()


# ============================================================
# Entry Point
# ============================================================

async def main():

    print()

    print("======================================")
    print("      RBAC DATABASE SEEDER")
    print("======================================")

    await seed_roles()

    print()
    print("RBAC Seed Completed Successfully.")
    print()


if __name__ == "__main__":
    asyncio.run(main())