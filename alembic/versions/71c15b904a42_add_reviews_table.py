"""add_reviews_table

Revision ID: 71c15b904a42
Revises: 7a62fc832732
Create Date: 2026-07-24 16:27:23.561935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71c15b904a42'
down_revision: Union[str, Sequence[str], None] = '7a62fc832732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "reviews",
        sa.Column("booking_id", sa.UUID(), nullable=False),
        sa.Column("property_id", sa.UUID(), nullable=False),
        sa.Column("customer_id", sa.UUID(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("owner_reply", sa.Text(), nullable=True),
        sa.Column("owner_replied_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_by", sa.UUID(), nullable=True),
        sa.Column("updated_by", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["booking_id"],
            ["bookings.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["property_id"],
            ["properties.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_reviews_booking_id"),
        "reviews",
        ["booking_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reviews_property_id"),
        "reviews",
        ["property_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reviews_customer_id"),
        "reviews",
        ["customer_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reviews_created_by"),
        "reviews",
        ["created_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reviews_updated_by"),
        "reviews",
        ["updated_by"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_reviews_updated_by"), table_name="reviews")
    op.drop_index(op.f("ix_reviews_created_by"), table_name="reviews")
    op.drop_index(op.f("ix_reviews_customer_id"), table_name="reviews")
    op.drop_index(op.f("ix_reviews_property_id"), table_name="reviews")
    op.drop_index(op.f("ix_reviews_booking_id"), table_name="reviews")
    op.drop_table("reviews")
