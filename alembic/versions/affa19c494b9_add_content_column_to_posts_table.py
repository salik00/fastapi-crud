"""add content column to posts table

Revision ID: affa19c494b9
Revises: a1a6fdc6a4d2
Create Date: 2025-01-18 19:55:07.948120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'affa19c494b9'
down_revision: Union[str, None] = 'a1a6fdc6a4d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', 
              sa.Column('content', sa.String(), nullable=False))
    

def downgrade() -> None:
    op.drop_column('posts', 'content')
    
