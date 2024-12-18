"""contacts new3

Revision ID: 09e8b61a8b02
Revises: d121f14da2c5
Create Date: 2024-12-15 21:04:46.677619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09e8b61a8b02'
down_revision: Union[str, None] = 'd121f14da2c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts_mod', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('users_mod', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_mod', 'updated_at')
    op.drop_column('contacts_mod', 'updated_at')
    # ### end Alembic commands ###
