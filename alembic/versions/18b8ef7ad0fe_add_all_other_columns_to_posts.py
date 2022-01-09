"""Add all other columns to posts

Revision ID: 18b8ef7ad0fe
Revises: dcdd5a2cc8be
Create Date: 2022-01-07 12:43:21.125401

"""
from re import T
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18b8ef7ad0fe'
down_revision = 'dcdd5a2cc8be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default=True))
    #op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    # op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
    pass
