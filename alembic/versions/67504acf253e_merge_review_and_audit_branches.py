"""Merge review and audit branches

Revision ID: 67504acf253e
Revises: ec237d86dbe6, 71c15b904a42
Create Date: 2026-07-26 09:41:51.719387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67504acf253e'
down_revision: Union[str, Sequence[str], None] = ('ec237d86dbe6', '71c15b904a42')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
