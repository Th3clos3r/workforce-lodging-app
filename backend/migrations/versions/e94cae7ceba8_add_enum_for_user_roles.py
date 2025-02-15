"""Add Enum for user roles

Revision ID: e94cae7ceba8
Revises: ef6a1c9407a9
Create Date: 2025-02-14 17:27:05.216530

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql
from alembic import op


# Create ENUM type for roles
user_roles = postgresql.ENUM('user', 'admin', name='user_roles', create_type=False)


def upgrade():
    # Ensure the ENUM type exists
    user_roles.create(op.get_bind(), checkfirst=True)

    # Alter the column and explicitly cast to ENUM
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'user' ")
    op.execute("UPDATE users SET role = 'user' WHERE role NOT IN ('user', 'admin')")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE user_roles USING role::user_roles")


def downgrade():
    op.execute('ALTER TABLE users ALTER COLUMN role TYPE VARCHAR USING role::TEXT')
    user_roles.drop(op.get_bind(), checkfirst=True)
# revision identifiers, used by Alembic.


revision: str = 'e94cae7ceba8'
down_revision: Union[str, None] = 'ef6a1c9407a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
