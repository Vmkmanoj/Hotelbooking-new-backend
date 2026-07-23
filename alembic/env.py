# ============================================================
# Standard Library
# ============================================================

from logging.config import fileConfig

# ============================================================
# Third Party
# ============================================================

from alembic import context
from sqlalchemy import create_engine, pool

# ============================================================
# Local Imports
# ============================================================

from app.core.config import settings
from app.database import Base

# ============================================================
# Alembic Configuration
# ============================================================

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.ALEMBIC_DATABASE_URL,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ============================================================
# Metadata
# ============================================================

target_metadata = Base.metadata

# ============================================================
# Offline Migrations
# ============================================================

def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    context.configure(
        url=settings.ALEMBIC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# Online Migrations
# ============================================================

def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = create_engine(
        settings.ALEMBIC_DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# Entry Point
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()