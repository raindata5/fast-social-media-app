"""first commit

Revision ID: 8a557052a8fe
Revises: 
Create Date: 2021-11-24 20:38:38.418849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a557052a8fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Post', sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
    sa.Column("title", sa.String(), nullable=False))
    


def downgrade():
    op.drop_table("Post")
    
