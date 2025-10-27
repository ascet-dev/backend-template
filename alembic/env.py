from adc_aiopg.alembic_env import run_alembic

import services.repositories
from settings import cfg

run_alembic(
    sqlalchemy_url=cfg.pg.connection.dsn,
    target_metadata=services.repositories.FitnessDAL.meta,
)
