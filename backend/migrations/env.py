from logging.config import fileConfig
import logging  # ✅ Import logging

from sqlalchemy import engine_from_config, pool
from alembic import context
from backend.database import DATABASE_URL
from backend.models import Base  # Base MUST be imported first!
import backend.models  # noqa: F401

# ✅ Set Metadata after models are imported
target_metadata = Base.metadata

# ✅ Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ✅ Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ✅ Setup Alembic logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# ✅ Log detected tables
logger.info(f"TARGET METADATA TABLES: {list(target_metadata.tables.keys())}")


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
