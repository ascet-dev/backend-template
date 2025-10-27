from adc_appkit import BaseApp, component
from adc_appkit.components.pg import PG

from services.repositories import DAO


class App(BaseApp):
    pg = component(PG, config_key="pg")

    @property
    def dao(self) -> DAO:
        if not hasattr(self, "_dao"):
            if not self.pg.is_alive():
                raise RuntimeError("PG is not alive")
            self._dao = DAO(self.pg)
        return self._dao

    async def _stop(self):
        pass

    async def business_logic(self):
        return await self.dao.pm.fetch("SELECT 1")
