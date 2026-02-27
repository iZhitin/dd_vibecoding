"""Add last_digest_at to user

Revision ID: 5e4c6e8f1234
Revises: d290a91a9145
Create Date: 2026-02-27 11:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e4c6e8f1234'
down_revision: Union[str, None] = 'd290a91a9145'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('last_digest_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'last_digest_at')
