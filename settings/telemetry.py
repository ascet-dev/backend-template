from pydantic import BaseModel


class JaegerExporterConnection(BaseModel):
    agent_host_name: str | None = None
    agent_port: int | None = None
    collector_endpoint: str | None = None
    username: str | None = None
    password: str | None = None
    udp_split_oversize_batches: bool = True


class Telemetry(BaseModel):
    jaeger_connection: JaegerExporterConnection
    enable: bool = False
