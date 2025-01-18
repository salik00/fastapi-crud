"""add foreign-key to posts table

Revision ID: c4917fb2e01a
Revises: 079cc8cda944
Create Date: 2025-01-18 21:32:57.604489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4917fb2e01a'
down_revision: Union[str, None] = '079cc8cda944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade():
    op.drop_constraints('posts_users_fk', table_name="posts")
    op.drop_table('posts','owner_id')
      
