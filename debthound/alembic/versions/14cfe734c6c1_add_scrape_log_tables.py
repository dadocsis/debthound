"""add scrape log tables

Revision ID: 14cfe734c6c1
Revises: d826484d85e8
Create Date: 2018-09-15 13:27:44.987275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14cfe734c6c1'
down_revision = 'd826484d85e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sitescrapelogdetails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('site_scrape_log_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('time_stamp', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['site_scrape_log_id'], ['sitescrapelog.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sitescrapelogdetails')
    # ### end Alembic commands ###