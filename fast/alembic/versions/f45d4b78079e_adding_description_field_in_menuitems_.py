"""Adding description field in MenuItems table

Revision ID: f45d4b78079e
Revises: 982169a090b6
Create Date: 2022-10-16 02:43:08.275296

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'f45d4b78079e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menuitems', sa.Column(
        'description', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menuitems', 'description')
    # ### end Alembic commands ###
