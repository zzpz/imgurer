"""create user table

Revision ID: 3f9c32a50ed7
Revises: 
Create Date: 2021-01-10 22:19:43.514244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f9c32a50ed7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date_created', sa.DateTime),
        sa.Column('hashed_password', sa.String()),
        sa.Column('username', sa.String, unique=True)
    )


def downgrade():
    pass
