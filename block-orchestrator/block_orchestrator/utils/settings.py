from pydantic_settings import BaseSettings, SettingsConfigDict


class BasicSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    HASH_CHALLENGE: str = "0000"
    
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_EXCHANGE: str = "blockchain"
    RABBITMQ_QUEUES: dict[str, str] = {
        "transactions": "tx",
        "blocks": "bl",
    }

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379  

    CONNECTION_MAX_RETRIES: int = 10
    CONNECTION_RETRY_DELAY: float = 5.5

Settings = BasicSettings()