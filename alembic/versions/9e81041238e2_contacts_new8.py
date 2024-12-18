"""contacts new8

Revision ID: 9e81041238e2
Revises: 1c48b68c7f37
Create Date: 2024-12-15 22:22:33.005130

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e81041238e2"
down_revision: Union[str, None] = "1c48b68c7f37"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users_mod",
        "expired_at",
        type_=sa.TIMESTAMP(timezone=False),  # Указываем новый тип
        existing_type=sa.DateTime(),  # Указываем текущий тип
        existing_nullable=True,
        postgresql_using="expired_at::timestamp without time zone",
    )  # Явное преобразование

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users_mod",
        "expired_at",
        existing_type=sa.DateTime(),
        type_=sa.VARCHAR(length=255),
        existing_nullable=True,
    )
    # ### end Alembic commands ###