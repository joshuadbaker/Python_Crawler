"""empty message

Revision ID: 101df08753
Revises: 352b4f2bc82
Create Date: 2015-12-16 13:57:51.237631

"""

# revision identifiers, used by Alembic.
revision = '101df08753'
down_revision = '352b4f2bc82'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('worker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['crawl.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('worker')
    op.drop_table('job')
    ### end Alembic commands ###
