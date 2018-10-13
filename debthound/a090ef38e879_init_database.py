"""init_database

Revision ID: a090ef38e879
Revises: 
Create Date: 2018-09-09 20:19:30.174000

"""
from alembic import op
from alembic import context
from alembic import command
from data_api.models import Base
from alembic.config import Config


# revision identifiers, used by Alembic.
revision = 'a090ef38e879'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ctx = op.get_context()
    c = context.get_x_argument(as_dictionary=True).get('url', None)
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("url", c.replace("sys", "debthound"))
    print('FUUUUUUUUUUUUUUUUUUCL!!!!!!!!!!!!!!!!!!!!')
    print(c)
    existing_databases = ctx.bind.execute("SHOW DATABASES;")
    if not next(iter([d[0] for d in existing_databases if d[0] == 'debthound']), None):
        ctx.bind.execute("CREATE DATABASE debthound")
    ctx.execute("USE debthound")
    Base.metadata.create_all(ctx.bind)
    command.stamp(alembic_cfg, "head")


def downgrade():
    pass
