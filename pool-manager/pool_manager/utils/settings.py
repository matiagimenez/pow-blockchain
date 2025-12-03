from pydantic_settings import BaseSettings, SettingsConfigDict


class BasicSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "password"
    RABBITMQ_EXCHANGE: str = "blockchain"
    RABBITMQ_TRANSACTIONS_QUEUE: str = "transactions"
    RABBITMQ_TRANSACTIONS_ROUTING_KEY: str = "tx"
    RABBITMQ_TASKS_QUEUE: str = "tasks"
    RABBITMQ_TASKS_ROUTING_KEY: str = "t"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    CONNECTION_MAX_RETRIES: int = 10
    CONNECTION_RETRY_DELAY: int = 5

    GCP_PROJECT_ID: str = "your-gcp-project-id"
    GCP_ZONE: str = "your-gcp-zone"
    GCP_CREDENTIALS_PATH: str = "your-gcp-credentials-path"
    GCP_INSTANCE_NAME_PREFIX: str = "miner-cpu"
    GCP_MACHINE_TYPE: str = "e2-highcpu-4"
    # Created with packer https://github.com/matiagimenez/pow-blockchain/tree/main/terraform/packer
    GCP_SOURCE_IMAGE: str = "pow-miner-1718748034"

    @property
    def GCP_MACHINE_FULL_TYPE(self) -> str:
        return f"zones/{self.GCP_ZONE}/machineTypes/{self.GCP_MACHINE_TYPE}"

    @property
    def GCP_VM_SOURCE_IMAGE(self) -> str:
        return f"projects/{self.GCP_PROJECT_ID}/global/images/{self.GCP_SOURCE_IMAGE}"

    @property
    def GCP_SUBNETWORK(self) -> str:
        return f"projects/{self.GCP_PROJECT_ID}/regions/{self.GCP_ZONE.rsplit('-', 1)[0]}/subnetworks/default"

    @property
    def CPU_MINER_STARTUP_SCRIPT(self) -> str:
        return (
            "#!/bin/bash\n"
            "sudo docker run -d -p 5000:5000 --name cpu-pow-miner pow-miner:latest"
        )


Settings = BasicSettings()
