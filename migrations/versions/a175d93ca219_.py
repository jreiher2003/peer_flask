"""empty message

Revision ID: a175d93ca219
Revises: 6bce76e72047
Create Date: 2016-12-19 10:50:59.342797

"""

# revision identifiers, used by Alembic.
revision = 'a175d93ca219'
down_revision = '6bce76e72047'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('NFLLogo', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('team', 'NFLLogo')
    # ### end Alembic commands ###
