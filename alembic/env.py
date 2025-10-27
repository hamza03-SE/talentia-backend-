from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Ajouter le chemin du projet

from app.core.config import get_settings
from app.db.base import Base  # Importer Base
# Importer tous les modèles pour Alembic
import app.models.user
import app.models.candidate
import app.models.offer

settings = get_settings()

# Config Alembic
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Utiliser l'URL depuis config.py
def run_migrations_offline():
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
