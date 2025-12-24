"""Add phone no to Social Media Table

Revision ID: 0514a646f9e6
Revises: 0b5251867b8d
Create Date: 2025-12-24 20:02:36.346541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0514a646f9e6'
down_revision: Union[str, Sequence[str], None] = '0b5251867b8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("Social_Media_Table_Relational",sa.Column("phone_no",sa.String(),sa.ForeignKey('Users.phone_no',ondelete='CASCADE',onupdate='NO ACTION'),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("Social_Media_Table_Relational","phone_no")
    pass
