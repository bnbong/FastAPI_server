"""First  migration

Revision ID: 292f9572b2a9
Revises: 
Create Date: 2022-07-22 15:21:59.634788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '292f9572b2a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table( 
        "users", 
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
        sa.Column("email", sa.String(length=255), unique=True, index=True), 
        sa.Column("hashed_password", sa.String(length=255)), 
        sa.Column("is_active", sa, Boolean(), default=True), 
        )


def downgrade():
    op.drop_table("users")
