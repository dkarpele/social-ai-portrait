"""schema

Revision ID: 83bbc8d0ca65
Revises: 
Create Date: 2024-08-08 16:42:52.308832

"""
from typing import Sequence, Union

from alembic import op
from db.pg_models.users import User

# revision identifiers, used by Alembic.
revision: str = '83bbc8d0ca65'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        User.id.expression,
        User.tg_chat_id.expression,
        User.tg_first_name.expression,
        User.tg_last_name.expression,
        User.disabled.expression,
        User.created_at.expression,
        User.modified_at.expression
    )


def downgrade() -> None:
    op.drop_table('users')

