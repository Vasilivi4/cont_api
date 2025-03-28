"""contacts new

Revision ID: b7fe1b0ad34d
Revises: 
Create Date: 2024-12-14 21:03:18.247429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7fe1b0ad34d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_mod',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_mod_email'), 'users_mod', ['email'], unique=True)
    op.create_index(op.f('ix_users_mod_id'), 'users_mod', ['id'], unique=False)
    op.create_table('contacts_mod',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('additional_info', sa.String(length=255), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users_mod.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contacts_mod_email'), 'contacts_mod', ['email'], unique=True)
    op.create_index(op.f('ix_contacts_mod_first_name'), 'contacts_mod', ['first_name'], unique=False)
    op.create_index(op.f('ix_contacts_mod_id'), 'contacts_mod', ['id'], unique=False)
    op.create_index(op.f('ix_contacts_mod_last_name'), 'contacts_mod', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_contacts_mod_last_name'), table_name='contacts_mod')
    op.drop_index(op.f('ix_contacts_mod_id'), table_name='contacts_mod')
    op.drop_index(op.f('ix_contacts_mod_first_name'), table_name='contacts_mod')
    op.drop_index(op.f('ix_contacts_mod_email'), table_name='contacts_mod')
    op.drop_table('contacts_mod')
    op.drop_index(op.f('ix_users_mod_id'), table_name='users_mod')
    op.drop_index(op.f('ix_users_mod_email'), table_name='users_mod')
    op.drop_table('users_mod')
    # ### end Alembic commands ###
