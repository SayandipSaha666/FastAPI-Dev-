"""Create Users Table

Revision ID: c317fe0e5844
Revises: 
Create Date: 2025-12-24 19:45:59.488992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c317fe0e5844'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'Users',
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column(
            "time",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=True
        ),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("username", name="uq_users_username"),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("Users")
    pass
