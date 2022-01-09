"""create users table

Revision ID: a168ce67d0be
Revises: 7bebf626a30d
Create Date: 2022-01-07 11:59:35.055351

"""
from re import T
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a168ce67d0be'
down_revision = '7bebf626a30d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False), 
                    sa.Column('email', sa.String(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
