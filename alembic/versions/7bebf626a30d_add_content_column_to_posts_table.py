"""add content_column_to_posts_table

Revision ID: 7bebf626a30d
Revises: 5f14bd19420c
Create Date: 2022-01-07 11:35:37.926951

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = '7bebf626a30d'
down_revision = '5f14bd19420c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts","content")
    pass
