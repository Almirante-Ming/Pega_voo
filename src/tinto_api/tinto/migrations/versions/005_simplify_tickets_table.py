"""006 - Simplify tickets table

Revision ID: 006_simplify_tickets
Revises: 005_add_flights_metadata
Create Date: 2025-12-02 10:00:00.000000

Removes temporal fields (boarding_time, arrival_time) and seat_number column.
Updates status field to VARCHAR(9) with 'disponível' default.

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '006_simplify_tickets'
down_revision: Union[str, None] = '005_add_flights_metadata'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - simplify tickets table."""
    # Drop columns that are no longer needed
    op.drop_column('tickets', 'boarding_time')
    op.drop_column('tickets', 'arrival_time')
    op.drop_column('tickets', 'seat_number')
    
    # Modify status column to be VARCHAR(9) with default 'disponível'
    op.alter_column('tickets', 'status',
               existing_type=sa.String(),
               type_=sa.String(9),
               existing_nullable=True,
               nullable=True,
               server_default='disponível')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('tickets', 'status',
               existing_type=sa.String(9),
               type_=sa.String(),
               existing_nullable=True,
               nullable=True)
    
    op.add_column('tickets', sa.Column('seat_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('tickets', sa.Column('arrival_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.add_column('tickets', sa.Column('boarding_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
