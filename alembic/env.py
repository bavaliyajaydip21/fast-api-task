import os
import sys
from logging.config import fileConfig
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config, pool
from alembic import context

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Add project root to sys.path BEFORE importing your models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.models import Base  # after path is set
target_metadata = Base.metadata

# Get Alembic config
config = context.config


# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Build DATABASE_URL dynamically
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Jaydip@21@")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")



DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Migration runners

def run_migrations_offline() -> None:
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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
