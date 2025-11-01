import asyncio
from logging import getLogger

from adc_aiopg.types import Base
from adc_webkit.web import Ctx, JsonEndpoint, Response
from adc_webkit.web.openapi import Doc

from services import App

logger = getLogger(__name__)


class LivenessResponse(Base):
    status: str


class Liveness(JsonEndpoint):
    doc = Doc(tags=["default"], summary="check if the server is running")

    response = Response(LivenessResponse)

    async def execute(self, ctx) -> dict:
        return {"status": "ok"}


class ReadinessResponse(Base):
    pg: bool
    # s3: bool
    # http: bool


class Readiness(JsonEndpoint):
    doc = Doc(tags=["default"], summary="check if the server is ready")

    response = Response(ReadinessResponse)

    async def execute(self, _) -> dict:
        """Собирает все компоненты и проверяет их готовность. PG, S3, HTTP, вызывает методы is_alive"""
        components = list(ReadinessResponse.__annotations__)
        statuses = await asyncio.gather(*(getattr(self.web.state.app, com).is_alive() for com in components))
        return dict(zip(components, statuses, strict=True))


### EXAMPLE


class DoResponse(Base):
    status: str


class Do(JsonEndpoint):
    doc = Doc(tags=["default"], summary="do something")

    response = Response(DoResponse)

    async def execute(self, ctx: Ctx) -> dict:
        app: App = ctx.request.app.state.app
        await app.do()
        return {"status": "ok"}
