"""Changed is_superuser column to is_caterer

Revision ID: 49b9618a1904
Revises: 83dc219fa37c
Create Date: 2022-09-20 08:17:22.967761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49b9618a1904'
down_revision = '83dc219fa37c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(column_name="is_superuser", new_column_name="is_caterer",table_name="users")


def downgrade() -> None:
    op.alter_column(column_name="is_caterer", new_column_name="is_superuser",table_name="users")
