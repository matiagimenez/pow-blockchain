from pydantic_settings import BaseSettings, SettingsConfigDict


class BasicSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_EXCHANGE: str = "blockchain"
    RABBITMQ_SUBTASKS_QUEUE: str = "subtasks"
    RABBITMQ_SUBTASKS_ROUTING_KEY: str = "st"

    CONNECTION_MAX_RETRIES: int = 10
    CONNECTION_RETRY_DELAY: int = 5
    KEEP_ALIVE_INTERVAL: int = 5

    POOL_MANAGER_URL: str = "http://pool-manager:5002"
    BLOCK_ORCHESTRATOR_URL: str = "http://block-orchestrator:5001"


Settings = BasicSettings()
