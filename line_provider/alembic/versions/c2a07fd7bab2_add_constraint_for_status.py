"""add constraint for status

Revision ID: c2a07fd7bab2
Revises: 5cf041621824
Create Date: 2024-12-09 23:20:00.963447

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c2a07fd7bab2'
down_revision: Union[str, None] = '5cf041621824'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'events',
        'status',
        type_=sa.Integer(),
        existing_type=sa.String(),
        existing_nullable=False,
        postgresql_using="status::integer"
    )

    op.create_check_constraint(
        'check_status_valid_values',
        'events',
        "status IN (1, 2, 3)"
    )

def downgrade():
    op.drop_constraint(
        'check_status_valid_values',
        'events',
        type_='check'
    )

    op.alter_column(
        'events',
        'status',
        type_=sa.String(),
        existing_type=sa.Integer(),
        existing_nullable=False,
        postgresql_using="status::text"
    )
