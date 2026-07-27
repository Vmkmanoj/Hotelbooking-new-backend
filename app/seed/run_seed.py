import asyncio

from app.database.session import AsyncSessionLocal
from app.seed.seed_data import seed_database


async def main():

    async with AsyncSessionLocal() as db:
        await seed_database(db)

    print("RBAC seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())