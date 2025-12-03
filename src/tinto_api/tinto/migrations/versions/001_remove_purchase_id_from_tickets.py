"""remove_purchase_id_from_tickets

Revision ID: 001_remove_purchase_id
Revises: dfd5e10710e3
Create Date: 2025-11-17 20:52:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_remove_purchase_id'
down_revision: Union[str, None] = 'dfd5e10710e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - remove purchase_id column from tickets."""
    # Use IF EXISTS to avoid errors
    op.execute("ALTER TABLE tickets DROP CONSTRAINT IF EXISTS tickets_purchase_id_fkey")
    op.execute("ALTER TABLE tickets DROP COLUMN IF EXISTS purchase_id")


def downgrade() -> None:
    """Downgrade schema - add purchase_id column back to tickets."""
    op.add_column('tickets', sa.Column('purchase_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key('tickets_purchase_id_fkey', 'tickets', 'purchase_history', ['purchase_id'], ['id'])
