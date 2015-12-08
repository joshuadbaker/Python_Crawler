"""empty message

Revision ID: 16b781edba9
Revises: 48b5c9d1815
Create Date: 2015-12-07 16:03:00.552906

"""

# revision identifiers, used by Alembic.
revision = '16b781edba9'
down_revision = '48b5c9d1815'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('crawl_id', sa.Integer(), nullable=True),
    sa.Column('image_all', postgresql.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['crawl_id'], ['crawl.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    ### end Alembic commands ###
