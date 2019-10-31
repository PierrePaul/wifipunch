"""Adds the hostname to the timelogs

Revision ID: 871ea1a262d7
Revises: 449e461c7b5f
Create Date: 2019-10-24 21:05:05.917518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '871ea1a262d7'
down_revision = '449e461c7b5f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('timelog', sa.Column('hostname', sa.String(), nullable=True))


def downgrade():
    op.drop_column('timelog', 'hostname')
