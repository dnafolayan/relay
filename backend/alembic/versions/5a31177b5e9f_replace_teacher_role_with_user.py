"""replace teacher role with user

Revision ID: 5a31177b5e9f
Revises: 22488831b071
Create Date: 2026-11-01 19:07:32.242566

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5a31177b5e9f"
down_revision: Union[str, Sequence[str], None] = "22488831b071"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE roleenum RENAME VALUE 'teacher' TO 'user'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE roleenum RENAME VALUE 'user' TO 'teacher'")
