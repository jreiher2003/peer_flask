"""empty message

Revision ID: c21b6eff505c
Revises: c9dd7b8a1028
Create Date: 2016-11-25 09:35:47.005922

"""

# revision identifiers, used by Alembic.
revision = 'c21b6eff505c'
down_revision = 'c9dd7b8a1028'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nfl_ml_bet', sa.Column('taken_network_fees', sa.Numeric(precision=8, scale=5), nullable=True))
    op.drop_column('nfl_ml_bet', 'network_fees')
    op.add_column('nfl_side_bet', sa.Column('taken_network_fees', sa.Numeric(precision=8, scale=5), nullable=True))
    op.drop_column('nfl_side_bet', 'network_fees')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nfl_side_bet', sa.Column('network_fees', sa.NUMERIC(precision=8, scale=5), autoincrement=False, nullable=True))
    op.drop_column('nfl_side_bet', 'taken_network_fees')
    op.add_column('nfl_ml_bet', sa.Column('network_fees', sa.NUMERIC(precision=8, scale=5), autoincrement=False, nullable=True))
    op.drop_column('nfl_ml_bet', 'taken_network_fees')
    ### end Alembic commands ###
