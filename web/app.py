from adc_webkit.web import Web
from adc_webkit.web.web import Route

from services import App
from settings import cfg
from web.endpoints import Do, Liveness, Readiness

app = App(
    components_config={
        "pg": cfg.pg.connection.model_dump(),
        "dao": {},
    },
)


class WebApp(Web):
    cors = cfg.app.cors.model_dump()
    routes = [
        Route("GET", "/readiness", Readiness),
        Route("GET", "/liveness", Liveness),
        Route("GET", "/do", Do),
    ]


web = WebApp.create(bindings={"app": app})
