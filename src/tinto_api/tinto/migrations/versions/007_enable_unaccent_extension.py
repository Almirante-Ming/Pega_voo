"""007 - Enable PostgreSQL unaccent extension

Revision ID: 007_enable_unaccent
Revises: 006_simplify_tickets
Create Date: 2025-12-02 23:40:00.000000

Enables the PostgreSQL unaccent extension for accent-insensitive text search
in flight queries (origin_city, destination_city).

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '007_enable_unaccent'
down_revision: Union[str, None] = '006_simplify_tickets'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - enable unaccent extension for accent-insensitive search."""
    # Enable the unaccent extension if not already enabled
    op.execute('CREATE EXTENSION IF NOT EXISTS unaccent')


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the unaccent extension
    op.execute('DROP EXTENSION IF EXISTS unaccent')
