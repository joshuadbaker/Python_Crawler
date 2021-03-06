"""empty message

Revision ID: 4aa215c325c
Revises: 3992f9e791d
Create Date: 2015-12-16 17:51:14.953178

"""

# revision identifiers, used by Alembic.
revision = '4aa215c325c'
down_revision = '3992f9e791d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job')
    op.drop_column('image', 'name')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_table('job',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('job_all', postgresql.JSON(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='job_pkey')
    )
    ### end Alembic commands ###
