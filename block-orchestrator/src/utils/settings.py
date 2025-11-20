from pydantic_settings import BaseSettings, SettingsConfigDict

class BasicSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    HASH_CHALLENGE: str = "0000"
    
    RABBITMQ_HOST: str = "rabbit"
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_EXCHANGE: str = "blockchain"
    RABBITMQ_MAX_RETRIES: int = 5
    RABBITMQ_RETRY_DELAY: int = 2
    RABBITMQ_QUEUES: dict[str, str] = {
        "transactions": "tx",
        "blocks": "bl",
    }

Settings = BasicSettings()