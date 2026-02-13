from logging import getLogger

from adc_appkit import BaseApp, ComponentStrategy, component
from adc_appkit.components.component import create_component
from adc_appkit.components.pg import PG

from services.repositories import DAO

logger = getLogger(__name__)


class App(BaseApp):
    pg = component(PG, config_key="pg")
    dao = component(
        create_component(DAO),
        dependencies={"pool": "pg"},
        config_key="dao",
        strategy=ComponentStrategy.REQUEST,
    )

    async def business_logic(self):
        return await self.dao.pm.fetch("SELECT 1")

    async def do(self):
        async with self.request_scope({}):
            res = await self.pg.obj.fetchval("SELECT 1")
            logger.info(res)

    async def _stop(self):
        pass
