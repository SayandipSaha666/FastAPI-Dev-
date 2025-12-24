"""Create Social Media Post Table

Revision ID: 06096d75b333
Revises: c317fe0e5844
Create Date: 2025-12-24 19:49:02.260030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06096d75b333'
down_revision: Union[str, Sequence[str], None] = 'c317fe0e5844'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('Social_Media_Table_Relational',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True,index=True),
                    sa.Column('title',sa.String(),nullable=False),
                    sa.Column('content',sa.String(),nullable=False),
                    sa.Column('published',sa.Boolean(),default=True),
                    sa.Column('time',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=True),
                    sa.Column('user_id',sa.Integer(),sa.ForeignKey('Users.id',ondelete='CASCADE',onupdate='NO ACTION'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('title')
                )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('Social_Media_Table_Relational')
    pass
