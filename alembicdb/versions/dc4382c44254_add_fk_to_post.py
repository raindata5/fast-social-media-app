"""add fk to post

Revision ID: dc4382c44254
Revises: 06aa1a2b30df
Create Date: 2021-11-25 21:56:04.837406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc4382c44254'
down_revision = '06aa1a2b30df'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Post", sa.Column("UserID", sa.Integer(), nullable=False))
    op.create_foreign_key('fk_post_user', source_table = "Post", referent_table="User", 
    local_cols = ['UserID'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('fk_post_user', table_name = "Post")
    op.drop_column("Post","UserID")
    pass
