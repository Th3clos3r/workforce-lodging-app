import os
from logging.config import fileConfig
from backend.database import Base
from sqlalchemy import engine_from_config, pool
# This import MUST come from alembic, not sqlalchemy
from alembic import context  # type: ignore


# This loads config from alembic.ini
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import your project's Base from wherever you define it
# Example: from backend.database import Base

# Provide the metadata object for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.run_migrations() here emit the given
    string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
