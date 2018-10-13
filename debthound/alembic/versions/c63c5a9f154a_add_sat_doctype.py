"""add SAT doctype

Revision ID: c63c5a9f154a
Revises: dcbe064d8294
Create Date: 2018-09-26 19:38:34.589570

"""
from alembic import op
import sqlalchemy as sa
from data_api.models import SiteDocType, Site
from sqlalchemy import orm


# revision identifiers, used by Alembic.
revision = 'c63c5a9f154a'
down_revision = 'dcbe064d8294'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    s = orm.Session(bind=bind)
    site = s.query(Site).filter_by(base_url='http://oris.co.palm-beach.fl.us').one()
    site_dtype = SiteDocType(
        name='SAT',
        description="Satisfaction"
    )
    site.doctypes.append(site_dtype)
    s.commit()

def downgrade():
    pass
