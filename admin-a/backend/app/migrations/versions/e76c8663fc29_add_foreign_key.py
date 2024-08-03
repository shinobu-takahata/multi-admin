"""Add foreign key

Revision ID: e76c8663fc29
Revises: e9734cca1da1
Create Date: 2024-07-20 07:36:39.307109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e76c8663fc29'
down_revision: Union[str, None] = 'e9734cca1da1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'items', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'items', type_='foreignkey')
    op.drop_column('items', 'user_id')
    # ### end Alembic commands ###