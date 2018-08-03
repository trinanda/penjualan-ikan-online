"""menghapus sifat unique pada kolom domisili pada table penjual

Revision ID: 3734e3e79491
Revises: 5275d8f1d2ef
Create Date: 2018-08-03 05:04:09.389422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3734e3e79491'
down_revision = '5275d8f1d2ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('penjual_domisili_key', 'penjual', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('penjual_domisili_key', 'penjual', ['domisili'])
    # ### end Alembic commands ###
