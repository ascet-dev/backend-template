from adc_webkit.web import Web
from adc_webkit.web.web import Route

from services import App
from settings import cfg
from web.endpoints import Liveness, Readiness

app = App(components_config={
    'pg': cfg.pg.connection.model_dump(),
})


class WebApp(Web):
    cors = cfg.app.cors.model_dump()
    routes = [
        Route("GET", "/readiness", Readiness),
        Route("GET", "/liveness", Liveness),
    ]


web = WebApp.create(bindings={'app': app})
