"""add few columns to posts table

Revision ID: 11e54e531698
Revises: c4917fb2e01a
Create Date: 2025-01-18 23:42:39.310163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11e54e531698'
down_revision: Union[str, None] = 'c4917fb2e01a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts",sa.Column('published',sa.Boolean(), nullable=False, server_default='true')),
    op.add_column("posts",sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False ))



def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    
