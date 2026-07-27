"""Refine domain model

Revision ID: 0657fe18252d
Revises: 67504acf253e
Create Date: 2026-07-26 19:59:01.654938

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0657fe18252d"
down_revision: Union[str, Sequence[str], None] = "67504acf253e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ----------------------------------------------------------
    # Create PostgreSQL Enum
    # ----------------------------------------------------------

    property_type_enum = sa.Enum(
        "HOTEL",
        "APARTMENT",
        "VILLA",
        "RESORT",
        "HOSTEL",
        "HOMESTAY",
        name="propertytype",
    )

    property_type_enum.create(op.get_bind(), checkfirst=True)

    # ----------------------------------------------------------
    # Property Type -> Enum
    # ----------------------------------------------------------

    op.execute(
        """
        ALTER TABLE properties
        ALTER COLUMN property_type
        TYPE propertytype
        USING property_type::propertytype;
        """
    )

    # ----------------------------------------------------------
    # Property
    # ----------------------------------------------------------

    op.create_unique_constraint(
        "uq_properties_address_id",
        "properties",
        ["address_id"],
    )

    # ----------------------------------------------------------
    # Property Images
    # ----------------------------------------------------------

    op.create_index(
        op.f("ix_property_images_display_order"),
        "property_images",
        ["display_order"],
        unique=False,
    )

    op.drop_column(
        "property_images",
        "is_primary",
    )

    # ----------------------------------------------------------
    # Reviews
    # ----------------------------------------------------------

    op.alter_column(
        "reviews",
        "created_by",
        existing_type=sa.UUID(),
        type_=sa.String(length=100),
        existing_nullable=True,
    )

    op.alter_column(
        "reviews",
        "updated_by",
        existing_type=sa.UUID(),
        type_=sa.String(length=100),
        existing_nullable=True,
    )

    # ----------------------------------------------------------
    # Room Images
    # ----------------------------------------------------------

    op.create_index(
        op.f("ix_room_images_display_order"),
        "room_images",
        ["display_order"],
        unique=False,
    )

    # ----------------------------------------------------------
    # Room Types
    # ----------------------------------------------------------

    op.create_unique_constraint(
        "uq_property_room_type",
        "room_types",
        ["property_id", "name"],
    )

    # ----------------------------------------------------------
    # Rooms
    # ----------------------------------------------------------

    op.drop_constraint(
        op.f("uq_room_type_room_number"),
        "rooms",
        type_="unique",
    )

    op.create_unique_constraint(
        "uq_property_room_number",
        "rooms",
        ["property_id", "room_number"],
    )

    # ----------------------------------------------------------
    # Users
    # ----------------------------------------------------------

    op.alter_column(
        "users",
        "role_id",
        existing_type=sa.UUID(),
        nullable=False,
    )

    op.create_unique_constraint(
        "uq_users_phone",
        "users",
        ["phone"],
    )

    op.drop_constraint(
        op.f("users_role_id_fkey"),
        "users",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_users_role_id_roles",
        "users",
        "roles",
        ["role_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    """Downgrade schema."""

    # ----------------------------------------------------------
    # Users
    # ----------------------------------------------------------

    op.drop_constraint(
        "fk_users_role_id_roles",
        "users",
        type_="foreignkey",
    )

    op.create_foreign_key(
        op.f("users_role_id_fkey"),
        "users",
        "roles",
        ["role_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.drop_constraint(
        "uq_users_phone",
        "users",
        type_="unique",
    )

    op.alter_column(
        "users",
        "role_id",
        existing_type=sa.UUID(),
        nullable=True,
    )

    # ----------------------------------------------------------
    # Rooms
    # ----------------------------------------------------------

    op.drop_constraint(
        "uq_property_room_number",
        "rooms",
        type_="unique",
    )

    op.create_unique_constraint(
        op.f("uq_room_type_room_number"),
        "rooms",
        ["room_type_id", "room_number"],
        postgresql_nulls_not_distinct=False,
    )

    # ----------------------------------------------------------
    # Room Types
    # ----------------------------------------------------------

    op.drop_constraint(
        "uq_property_room_type",
        "room_types",
        type_="unique",
    )

    # ----------------------------------------------------------
    # Room Images
    # ----------------------------------------------------------

    op.drop_index(
        op.f("ix_room_images_display_order"),
        table_name="room_images",
    )

    # ----------------------------------------------------------
    # Reviews
    # ----------------------------------------------------------

    op.alter_column(
        "reviews",
        "updated_by",
        existing_type=sa.String(length=100),
        type_=sa.UUID(),
        existing_nullable=True,
    )

    op.alter_column(
        "reviews",
        "created_by",
        existing_type=sa.String(length=100),
        type_=sa.UUID(),
        existing_nullable=True,
    )

    # ----------------------------------------------------------
    # Property Images
    # ----------------------------------------------------------

    op.add_column(
        "property_images",
        sa.Column(
            "is_primary",
            sa.BOOLEAN(),
            nullable=False,
        ),
    )

    op.drop_index(
        op.f("ix_property_images_display_order"),
        table_name="property_images",
    )

    # ----------------------------------------------------------
    # Property
    # ----------------------------------------------------------

    op.drop_constraint(
        "uq_properties_address_id",
        "properties",
        type_="unique",
    )

    op.execute(
        """
        ALTER TABLE properties
        ALTER COLUMN property_type
        TYPE VARCHAR(100)
        USING property_type::text;
        """
    )

    property_type_enum = sa.Enum(
        "HOTEL",
        "APARTMENT",
        "VILLA",
        "RESORT",
        "HOSTEL",
        "HOMESTAY",
        name="propertytype",
    )

    property_type_enum.drop(op.get_bind(), checkfirst=True)