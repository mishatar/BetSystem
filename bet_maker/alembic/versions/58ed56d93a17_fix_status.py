"""fix status

Revision ID: 58ed56d93a17
Revises: 783870cdc0f8
Create Date: 2024-12-11 04:35:22.309898

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '58ed56d93a17'
down_revision: Union[str, None] = '783870cdc0f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.alter_column(
        'bets',
        'status',
        type_=sa.Integer(),
        existing_type=sa.String(),
        existing_nullable=False,
        postgresql_using="status::integer"
    )

    op.create_check_constraint(
        'check_status_valid_values',
        'bets',
        "status IN (1, 2, 3)"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bets', 'status',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               nullable=True,
               comment=None,
               existing_comment='1 - NEW, 2 - FINISHED_WIN, 3 - FINISHED_LOSE')
    # ### end Alembic commands ###