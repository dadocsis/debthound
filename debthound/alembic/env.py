from __future__ import with_statement
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from logging.config import fileConfig


from data_api.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def exclude_tables_from_config(config_):
    tables_ = config_.get("tables", None)
    if tables_ is not None:
        tables = tables_.split(",")
    return tables


exclude_tables = exclude_tables_from_config(config.get_section('alembic:exclude'))


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in exclude_tables:
        return False
    else:
        return True

def get_url():
    url = context.get_x_argument(as_dictionary=True).get('url')
    assert url, "Database URL must be specified on command line with -x url=<DB_URL>"
    return url


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, include_object=include_object)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = make_url(get_url())
    database = url.database
    url.database = "sys"
    connectable = create_engine(url)
    existing_databases = connectable.execute("SHOW DATABASES;")

    if not next(iter([d[0] for d in existing_databases if d[0] == database]), None):
        connectable.execute("CREATE DATABASE {0}".format(database))

    url.database = database
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
