"""> MenuItem.item_name is now unique

Revision ID: 81f15daaa73d
Revises: 6ae631b4cad7
Create Date: 2022-10-16 10:16:21.048379

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision = '81f15daaa73d'
down_revision = '6ae631b4cad7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'menuitems', ['item_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'menuitems', type_='unique')
    # ### end Alembic commands ###
