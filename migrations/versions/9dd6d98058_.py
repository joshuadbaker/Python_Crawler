"""empty message

Revision ID: 9dd6d98058
Revises: 3d8fe5e3cac
Create Date: 2015-12-08 13:12:15.052266

"""

# revision identifiers, used by Alembic.
revision = '9dd6d98058'
down_revision = '3d8fe5e3cac'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crawl', sa.Column('crawl_all', postgresql.JSON(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('crawl', 'crawl_all')
    ### end Alembic commands ###
