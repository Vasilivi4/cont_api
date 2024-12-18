"""contacts new1

Revision ID: 7ab7bd5087e9
Revises: b7fe1b0ad34d
Create Date: 2024-12-15 20:52:13.805590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ab7bd5087e9'
down_revision: Union[str, None] = 'b7fe1b0ad34d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users_mod', sa.Column('access_token', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_mod', 'access_token')
    # ### end Alembic commands ###