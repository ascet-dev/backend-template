from pydantic import Field
from pydantic_settings import BaseSettings


class Connection(BaseSettings):
    url: str = "http://localhost:9000"
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"


class S3(BaseSettings):
    connection: Connection = Field(default_factory=Connection)
    bucket: str = "bucket"
