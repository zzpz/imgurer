"""Add (seaweedFS) fid column to images table

Revision ID: 52b958cefc48
Revises: 39876a695438
Create Date: 2021-01-22 12:05:35.186737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52b958cefc48"
down_revision = "39876a695438"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("images", sa.Column("fid", sa.String))


def downgrade():
    op.drop_column("images", "fid")
