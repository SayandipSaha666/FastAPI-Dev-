"""Create Votes Table

Revision ID: 975cf8534282
Revises: 06096d75b333
Create Date: 2025-12-24 19:50:55.370422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '975cf8534282'
down_revision: Union[str, Sequence[str], None] = '06096d75b333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "Votes",
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey(
                "Users.id",
                ondelete="CASCADE",
                onupdate="NO ACTION"
            ),
            primary_key=True
        ),
        sa.Column(
            "post_id",
            sa.Integer(),
            sa.ForeignKey(
                "Social_Media_Table_Relational.id",
                ondelete="CASCADE",
                onupdate="NO ACTION"
            ),
            primary_key=True
        )
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("Votes")
    pass
