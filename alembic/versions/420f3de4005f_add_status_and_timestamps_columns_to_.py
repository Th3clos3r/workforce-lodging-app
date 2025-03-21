"""Add status and timestamps columns to Bookings



Revision ID: 420f3de4005f
Revises: e1f1a6cc121c
Create Date: 2025-03-19 16:44:41.396683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '420f3de4005f'
down_revision: Union[str, None] = 'e1f1a6cc121c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_lodgings_id', table_name='lodgings')
    op.drop_table('lodgings')
    op.drop_index('ix_bookings_id', table_name='bookings')
    op.drop_table('bookings')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lodging_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('check_in_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('check_out_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('total_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('pending', 'confirmed', 'canceled', name='booking_status'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['lodging_id'], ['lodgings.id'], name='bookings_lodging_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='bookings_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='bookings_pkey')
    )
    op.create_index('ix_bookings_id', 'bookings', ['id'], unique=False)
    op.create_table('lodgings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price_per_night', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('availability', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='lodgings_pkey')
    )
    op.create_index('ix_lodgings_id', 'lodgings', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('role', postgresql.ENUM('user', 'admin', name='user_roles'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###
