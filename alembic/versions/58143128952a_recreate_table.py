"""recreate table

Revision ID: 58143128952a
Revises: 18b8ef7ad0fe
Create Date: 2022-01-07 13:11:11.116834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58143128952a'
down_revision = '18b8ef7ad0fe'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),server_default='TRUE', nullable=False))
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True),  server_default=sa.text('NOW()'),nullable=False))
    pass

def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
    pass
