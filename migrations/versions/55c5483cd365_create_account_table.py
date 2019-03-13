"""create account table

Revision ID: 55c5483cd365
Revises: 
Create Date: 2019-03-13 11:48:15.685175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "55c5483cd365"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
    )


def downgrade():
    op.drop_table("users")
