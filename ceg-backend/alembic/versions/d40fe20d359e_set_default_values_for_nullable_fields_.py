"""Set default values for nullable fields in socios

Revision ID: d40fe20d359e
Revises: 5720c68e82d2
Create Date: 2024-07-30 18:35:38.089807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd40fe20d359e'
down_revision: Union[str, None] = '5720c68e82d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
