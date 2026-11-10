"""update field min and max lengths

Revision ID: 966d106b6dec
Revises: 032ebcb674a7
Create Date: 2026-11-10 16:55:12.684979

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "966d106b6dec"
down_revision: Union[str, Sequence[str], None] = "032ebcb674a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "first_name",
        existing_type=sa.String(),
        type_=sa.String(50),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "last_name",
        existing_type=sa.String(),
        type_=sa.String(50),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(),
        type_=sa.String(255),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(),
        type_=sa.String(255),
        existing_nullable=False,
    )

    op.alter_column(
        "schools",
        "name",
        existing_type=sa.String(),
        type_=sa.String(150),
        existing_nullable=False,
    )
    op.alter_column(
        "schools",
        "email",
        existing_type=sa.String(),
        type_=sa.String(255),
        existing_nullable=False,
    )
    op.alter_column(
        "schools",
        "phone_number",
        existing_type=sa.String(),
        type_=sa.String(32),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "schools",
        "phone_number",
        existing_type=sa.String(32),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "schools",
        "email",
        existing_type=sa.String(255),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "schools",
        "name",
        existing_type=sa.String(150),
        type_=sa.String(),
        existing_nullable=False,
    )

    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(255),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(255),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "last_name",
        existing_type=sa.String(50),
        type_=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "first_name",
        existing_type=sa.String(50),
        type_=sa.String(),
        existing_nullable=False,
    )
