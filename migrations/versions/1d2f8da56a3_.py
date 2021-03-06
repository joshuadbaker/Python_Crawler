"""empty message

Revision ID: 1d2f8da56a3
Revises: 19b3057eb63
Create Date: 2015-12-18 11:23:11.644390

"""

# revision identifiers, used by Alembic.
revision = '1d2f8da56a3'
down_revision = '19b3057eb63'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('result_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['result_id'], ['result.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('crawl_result_id_fkey', 'crawl', type_='foreignkey')
    op.drop_column('crawl', 'result_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crawl', sa.Column('result_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('crawl_result_id_fkey', 'crawl', 'result', ['result_id'], ['id'])
    op.drop_table('task')
    ### end Alembic commands ###
