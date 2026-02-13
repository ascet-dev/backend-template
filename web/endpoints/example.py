from adc_aiopg.types import Base
from adc_webkit.web import Ctx, JsonEndpoint, Response
from adc_webkit.web.openapi import Doc

from services import App


class DoResponse(Base):
    status: str


class Do(JsonEndpoint):
    doc = Doc(tags=["example"], summary="do something")

    response = Response(DoResponse)

    async def execute(self, ctx: Ctx) -> dict:
        app: App = ctx.request.app.state.app
        await app.do()
        return {"status": "ok"}
