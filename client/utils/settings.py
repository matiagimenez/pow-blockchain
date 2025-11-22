from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings_(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BLOCK_ORCHESTRATOR_URL: str = "http://localhost:8000"

    TRANSACTIONS_PER_BATCH: int = 10
    BATCH_INTERVAL_SECONDS: int = 225  # 3 * 75 seconds


Settings = Settings_()
