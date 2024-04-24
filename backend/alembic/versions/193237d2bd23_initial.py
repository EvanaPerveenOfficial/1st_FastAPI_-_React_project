"""initial

Revision ID: 193237d2bd23
Revises: 71be95ad18f2
Create Date: 2024-04-23 09:46:17.511406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '193237d2bd23'
down_revision: Union[str, None] = '71be95ad18f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
