"""new column for post

Revision ID: d9768aa1e103
Revises: 8a557052a8fe
Create Date: 2021-11-24 21:02:30.030127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import false


# revision identifiers, used by Alembic.
revision = 'd9768aa1e103'
down_revision = '8a557052a8fe'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Post", sa.Column("Content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("Post", "Content")
