"""create users images

Revision ID: 39876a695438
Revises: 
Create Date: 2021-01-20 14:59:32.145408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "39876a695438"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("date_created", sa.DateTime),
        sa.Column("hashed_password", sa.String),
        sa.Column("username", sa.String, unique=True),
    )

    op.create_table(
        "images",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("date_created", sa.DateTime),
        sa.Column("parsed", sa.Boolean, default=False),
        sa.Column("dhash128", sa.String),
        sa.Column("filename", sa.String),
        sa.Column("url", sa.String),
        sa.Column("url_thumb", sa.String),
        sa.Column("in_bktree", sa.Boolean, default=False),
    )
