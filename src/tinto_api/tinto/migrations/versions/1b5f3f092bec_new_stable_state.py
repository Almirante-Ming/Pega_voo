"""new_stable_state - final database state migration

Revision ID: 1b5f3f092bec
Revises:
Create Date: 2025-11-26 10:58:54.284352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b5f3f092bec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - create final database state from base schema."""

    op.create_table('airlines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('active', 'inactive', 'deleted', name='airline_status', native_enum=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_airlines_id'), 'airlines', ['id'], unique=False)

    op.create_table('flights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('airline_id', sa.Integer(), nullable=False),
    sa.Column('flight_number', sa.String(), nullable=False),
    sa.Column('aircraft_model', sa.String(), nullable=False),
    sa.Column('origin_city', sa.String(), nullable=False),
    sa.Column('origin_airport', sa.String(), nullable=False),
    sa.Column('destination_city', sa.String(), nullable=False),
    sa.Column('destination_airport', sa.String(), nullable=False),
    sa.Column('departure_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('estimated_arrival', sa.DateTime(timezone=True), nullable=False),
    sa.Column('stops_count', sa.Integer(), nullable=False),
    sa.Column('avaliable_seats', sa.Integer(), nullable=False),
    sa.Column('economy_seats', sa.Integer(), nullable=False),
    sa.Column('premium_seats', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('scheduled', 'cancelled', name='flight_status', native_enum=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['airline_id'], ['airlines.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('flight_number')
    )
    op.create_index(op.f('ix_flights_id'), 'flights', ['id'], unique=False)

    op.create_table('seats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('seat_number', sa.String(), nullable=False),
    sa.Column('seat_class', sa.Enum('economy', 'business', 'executive', 'first', name='seat_class_enum', native_enum=False), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('flight_id', 'seat_number', name='unique_flight_seat')
    )
    op.create_index(op.f('ix_seats_id'), 'seats', ['id'], unique=False)

    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('passenger_id', sa.Integer(), nullable=False),
    sa.Column('seat_class', sa.Enum('economy', 'business', 'executive', 'first', name='seat_class', native_enum=False), nullable=False),
    sa.Column('seat_number', sa.String(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('boarding_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('arrival_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('status', sa.Enum('marked', 'reserved', 'cancelled', 'completed', name='booking_status', native_enum=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.ForeignKeyConstraint(['passenger_id'], ['persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=False)
    
    op.create_table('ticket_status_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('old_status', sa.Enum('marked', 'reserved', 'cancelled', 'completed', name='old_status', native_enum=False), nullable=False),
    sa.Column('new_status', sa.Enum('marked', 'reserved', 'cancelled', 'completed', name='new_status', native_enum=False), nullable=False),
    sa.Column('changed_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('changed_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['changed_by'], ['persons.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_status_log_id'), 'ticket_status_log', ['id'], unique=False)
    
    op.add_column('persons', sa.Column('full_name', sa.String(), nullable=False))
    op.add_column('persons', sa.Column('birth_date', sa.String(), nullable=False))
    op.add_column('persons', sa.Column('phone_number', sa.String(), nullable=False))
    op.add_column('persons', sa.Column('status', sa.Enum('active', 'inactive', 'deleted', name='user_status', native_enum=False), nullable=True))
    op.add_column('persons', sa.Column('person_type', sa.Enum('customer', 'company_admin', 'sysadmin', name='user_type', native_enum=False), nullable=True))
    op.add_column('persons', sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender', native_enum=False), nullable=False))
    op.add_column('persons', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('persons', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('persons', 'name')
    op.drop_column('persons', 'phone')
    op.drop_column('persons', 'state')
    op.drop_column('persons', 'p_type')
    op.drop_column('persons', 'dt_birth')
    op.drop_column('persons', 'dt_create')
    op.drop_column('persons', 'dt_update')
    
    op.execute("""
        INSERT INTO persons (
            id,
            cpf,
            email,
            hashed_password,
            gender,
            full_name,
            birth_date,
            phone_number,
            status,
            person_type,
            created_at,
            updated_at
        ) VALUES (
            0,
            '789.417.690-78',
            'super@admin.com',
            '$argon2id$v=19$m=65536,t=3,p=4$oFSq9f4fA0CIcW5NSendmw$lWTkgXFinVyc4BUY7oB+UpFphEF3iuB04za2HeveX7w',
            'male',
            'SA',
            '1999-12-31',
            '99999999999',
            'active',
            'sysadmin',
            '2025-10-31 15:07:23.195-04',
            '2025-10-31 15:07:23.195-04'
        );
    """)


def downgrade() -> None:
    """Downgrade schema - revert to base persons table."""

    op.execute("DELETE FROM persons WHERE id = 0")
    
    op.drop_index(op.f('ix_ticket_status_log_id'), table_name='ticket_status_log')
    op.drop_table('ticket_status_log')

    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')

    op.drop_index(op.f('ix_seats_id'), table_name='seats')
    op.drop_table('seats')

    op.drop_index(op.f('ix_flights_id'), table_name='flights')
    op.drop_table('flights')

    op.drop_index(op.f('ix_airlines_id'), table_name='airlines')
    op.drop_table('airlines')
    
    op.drop_table('persons')
