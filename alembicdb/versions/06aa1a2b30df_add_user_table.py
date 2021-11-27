"""add user table

Revision ID: 06aa1a2b30df
Revises: d9768aa1e103
Create Date: 2021-11-25 21:42:18.255166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06aa1a2b30df'
down_revision = 'd9768aa1e103'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('User',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('User')
    pass
