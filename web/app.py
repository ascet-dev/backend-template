from adc_webkit.web import Web
from adc_webkit.web.web import Route

from services import App
from settings import cfg
from web import endpoints as e

app = App(
    components_config={
        "pg": cfg.pg.connection.model_dump(),
        "dao": {},
    },
)


class WebApp(Web):
    cors = cfg.app.cors.model_dump()
    routes = [
        # health
        Route("GET", "/readiness", e.Readiness),
        Route("GET", "/liveness", e.Liveness),
        # example
        Route("GET", "/do", e.Do),
    ]


web = WebApp.create(bindings={"app": app})
