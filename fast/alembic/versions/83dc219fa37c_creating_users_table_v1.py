"""Creating users table_V1

Revision ID: 83dc219fa37c
Revises: 
Create Date: 2022-09-04 12:23:31.687209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83dc219fa37c'
down_revision = None
branch_labels = None
depends_on = None


#     uid = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     username = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     email_address = Column(String, unique=True, nullable=False)
#     cell_no = Column(String, unique=True, nullable=False)
#     is_active = Column(Boolean, nullable=False)
#     is_admin = Column(Boolean, nullable=False)
#     is_superuser = Column(Boolean, nullable=False)
#     created_at = Column(DateTime, nullable=False)
#     last_logged_in = Column(DateTime, nullable=False)


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('uid', sa.String(255), primary_key=True),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.String(500), nullable=False),
        sa.Column('email_address', sa.String(255),unique=True, nullable=False),
        sa.Column('cell_no', sa.String(255), nullable=False, unique=True),
        sa.Column('is_active', sa.Boolean, nullable=False),
        sa.Column('is_admin', sa.Boolean, nullable=False),
        sa.Column('is_superuser', sa.Boolean, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('last_logged_in', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
