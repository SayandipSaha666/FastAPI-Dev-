"""Add phone no to Users

Revision ID: 0b5251867b8d
Revises: 975cf8534282
Create Date: 2025-12-24 19:52:42.404098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b5251867b8d'
down_revision: Union[str, Sequence[str], None] = '975cf8534282'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
    "Users",
    sa.Column("phone_no", sa.String(), nullable=True)
    )

    op.create_unique_constraint(
        "uq_users_phone_no",
        "Users",
        ["phone_no"]
    )

    op.alter_column(
        "Users",
        "phone_no",
        nullable=False
    )
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("Users","phone_no")
    pass
