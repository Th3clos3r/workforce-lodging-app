from alembic import op
import sqlalchemy as sa

revision = "ef6a1c9407a9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'lodgings',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('price_per_night', sa.Float(), nullable=False),
        sa.Column('availability', sa.Boolean(), default=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(),
                  onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table('lodgings')
