"""Add forerign key to posts table

Revision ID: dcdd5a2cc8be
Revises: a168ce67d0be
Create Date: 2022-01-07 12:22:17.827914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcdd5a2cc8be'
down_revision = 'a168ce67d0be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('post_owner',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users', 
    local_cols=['post_owner'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','post_owner')
    pass
