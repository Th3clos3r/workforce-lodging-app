from alembic import op
import sqlalchemy as sa

revision = 'ef6a1c9407a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply migration: Add 'role' column with default 'user'"""
    op.add_column(
        "users",
        sa.Column("role", sa.String(), nullable=False, server_default="user"),
    )

    op.alter_column(
        "users",
        "email",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )


def downgrade() -> None:
    """Rollback migration: Remove 'role' column"""
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )

    op.alter_column(
        "users",
        "email",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )

    op.drop_column("users", "role")
