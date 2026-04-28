from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from core.config import settings
from common.model import Base
from app.admin.model.sync import Synchronization
from app.admin.model.user import User
from app.admin.model.salary_increase import SalaryIncrease
from app.reports.model.report import Report
from app.admin.model.user_permission import UserPermission
from app.admin.model.role import Role
from app.admin.model.role_permission import RolePermission
from app.admin.model.store import Store
from app.reports.model.retail_store import RetailStore
from app.directories.model.payment_purpose import PaymentPurpose
from app.reports.model.payment_journal import PaymentJournal
# from app.dashboard.model.retail_demand import RetailDemand
from app.directories.model.bonus import Bonus
from app.directories.model.salary import SalaryCondition
from app.testing.model.choice import Choice
from app.testing.model.question import Question
from app.testing.model.test import Test
from app.testing.model.test_result import TestResult
from app.testing.model.user_answer import UserAnswer

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.database_url_alembic)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
