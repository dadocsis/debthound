"""init_database

Revision ID: a090ef38e879
Revises: 
Create Date: 2018-09-09 20:19:30.174000

"""
from alembic import op
import sqlalchemy as sa
from debthound.data_api.models import Base


# revision identifiers, used by Alembic.
revision = 'a090ef38e879'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ctx = op.get_context()
    ctx.bind.execute("CREATE DATABASE debthound")
    ctx.execute("USE debthound")
    Base.metadata.create_all(ctx.bind)


def downgrade():
    pass
