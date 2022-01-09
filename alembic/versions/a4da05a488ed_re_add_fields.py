"""re-add fields

Revision ID: a4da05a488ed
Revises: 58143128952a
Create Date: 2022-01-07 15:53:22.851399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4da05a488ed'
down_revision = '58143128952a'
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