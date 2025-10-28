from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from api.db.base import Base
from api.db.models.cell_tower import CellTower
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

POSTGRES_USER = os.getenv("POSTGRES_USER", "ben")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test")

# Use psycopg2 for Alembic (synchronous driver)
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# --- Restrict autogenerate to your models only ---
metadata_table_names = set(Base.metadata.tables.keys())


def include_object(obj, name, type_, reflected, compare_to):
    if type_ == "table" and name not in metadata_table_names:
        return False
    return True


def _filter_directives(context, revision, directives):
    """Silently drop empty migration files"""
    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []


# --- Offline mode ---
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        include_schemas=False,
        process_revision_directives=_filter_directives,
    )
    with context.begin_transaction():
        context.run_migrations()


# --- Online mode ---
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            include_schemas=False,
            compare_type=True,
            compare_server_default=True,
            process_revision_directives=_filter_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
