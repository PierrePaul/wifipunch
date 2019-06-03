"""empty message

Revision ID: bceabfde0ee7
Revises: 2dc510fd2b1e
Create Date: 2019-05-21 16:02:48.642265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bceabfde0ee7'
down_revision = '2dc510fd2b1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('macaddress', sa.Column('mac_address', sa.String(), nullable=True))
    op.add_column('macaddress', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('macaddress_mac_key', 'macaddress', type_='unique')
    op.create_unique_constraint(None, 'macaddress', ['mac_address'])
    op.create_foreign_key(None, 'macaddress', 'user', ['user_id'], ['id'])
    op.drop_column('macaddress', 'mac')
    op.add_column('timelog', sa.Column('mac_addresses_id', sa.Integer(), nullable=True))
    op.add_column('timelog', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'timelog', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'timelog', 'macaddress', ['mac_addresses_id'], ['id'])
    op.drop_constraint('user_mac_addresses_id_fkey', 'user', type_='foreignkey')
    op.drop_column('user', 'mac_addresses_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('mac_addresses_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_mac_addresses_id_fkey', 'user', 'macaddress', ['mac_addresses_id'], ['id'])
    op.drop_constraint(None, 'timelog', type_='foreignkey')
    op.drop_constraint(None, 'timelog', type_='foreignkey')
    op.drop_column('timelog', 'user_id')
    op.drop_column('timelog', 'mac_addresses_id')
    op.add_column('macaddress', sa.Column('mac', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'macaddress', type_='foreignkey')
    op.drop_constraint(None, 'macaddress', type_='unique')
    op.create_unique_constraint('macaddress_mac_key', 'macaddress', ['mac'])
    op.drop_column('macaddress', 'user_id')
    op.drop_column('macaddress', 'mac_address')
    # ### end Alembic commands ###