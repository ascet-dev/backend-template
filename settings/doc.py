from pydantic_settings import BaseSettings


class Doc(BaseSettings):
    title: str = "AppName"
    version: str = "0.0.1"
    route: str = "/doc.json"
    schemes: list[str] = ["http", "https"]
