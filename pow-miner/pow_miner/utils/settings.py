from pydantic_settings import BaseSettings, SettingsConfigDict


class BasicSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_EXCHANGE: str = "blockchain"
    RABBITMQ_TASKS_QUEUE: str = "tasks"
    RABBITMQ_TASKS_ROUTING_KEY: str = "t"

    CONNECTION_MAX_RETRIES: int = 10
    CONNECTION_RETRY_DELAY: int = 5
    KEEP_ALIVE_INTERVAL: int = 5

    BLOCK_ORCHESTRATOR_URL: str = "http://localhost:8000"
    POOL_MANAGER_URL: str = "http://localhost:7000"


Settings = BasicSettings()
