"""finish cols for Post

Revision ID: 4eb5a0571f48
Revises: dc4382c44254
Create Date: 2021-11-25 22:09:46.859477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eb5a0571f48'
down_revision = 'dc4382c44254'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Post', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('Post', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('Post', "published")
    op.drop_column('Post', "created_at")

    pass
