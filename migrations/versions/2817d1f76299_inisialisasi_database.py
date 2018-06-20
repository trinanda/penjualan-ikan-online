"""inisialisasi database

Revision ID: 2817d1f76299
Revises: 
Create Date: 2018-06-20 01:36:14.022913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2817d1f76299'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ikan', sa.Column('urutan_ikan_dalam_tampilan_halaman', sa.Integer(), nullable=True))
    op.drop_column('ikan', 'urutan_ikan')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ikan', sa.Column('urutan_ikan', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('ikan', 'urutan_ikan_dalam_tampilan_halaman')
    # ### end Alembic commands ###
