import time
from typing import Any, Optional

from google.cloud import compute_v1
from google.oauth2 import service_account

from pool_manager.utils import Settings, logger


class GoogleCloudClient:
    """Manages Google Cloud Compute Engine instances for mining operations."""

    def __init__(self, credentials_path: Optional[str] = Settings.GCP_CREDENTIALS_PATH):
        self.credentials_path = credentials_path
        self._credentials = None
        self._client = None

    @property
    def credentials(self) -> service_account.Credentials:
        if self._credentials is None:
            self._credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
        return self._credentials

    @property
    def client(self) -> compute_v1.InstancesClient:
        if self._client is None:
            self._client = compute_v1.InstancesClient(credentials=self.credentials)
        return self._client

    @property
    def vm_config(self) -> dict[str, Any]:
        return {
            "name": f"{Settings.GCP_INSTANCE_NAME_PREFIX}{int(time.time())}",
            "machine_type": Settings.GCP_MACHINE_FULL_TYPE,
            "disks": [
                {
                    "boot": True,
                    "auto_delete": True,
                    "initialize_params": {
                        "source_image": Settings.GCP_VM_SOURCE_IMAGE,
                    },
                }
            ],
            "network_interfaces": [
                {
                    "subnetwork": Settings.GCP_SUBNETWORK,
                    "access_configs": [{"name": "External NAT"}],
                }
            ],
            "metadata": {
                "items": [
                    {
                        "key": "startup-script",
                        "value": Settings.CPU_MINER_STARTUP_SCRIPT,
                    }
                ]
            },
        }

    def create_multiple_instances(self, number_of_instances: int) -> None:
        """
        Create multiple compute instances for mining.
        """
        for n in range(number_of_instances):
            logger.info(f"Creating instance {n + 1}/{number_of_instances}...")
            self.client.insert(
                project=Settings.GCP_PROJECT_ID,
                zone=Settings.GCP_ZONE,
                instance_resource=self.vm_config,
            )
            time.sleep(0.1)  # Ensure unique timestamps

        logger.info(f"Successfully created {number_of_instances} instance(s).")

    def get_active_instance_count(self) -> int:
        """Count the number of running instances in the configured zone."""
        instance_list = self.client.list(
            project=Settings.GCP_PROJECT_ID,
            zone=Settings.GCP_ZONE,
        )
        return sum(1 for instance in instance_list if instance.status == "RUNNING")

    def destroy_all_instances(self) -> None:
        """Delete all instances in the configured zone."""
        instance_list = self.client.list(
            project=Settings.GCP_PROJECT_ID, zone=Settings.GCP_ZONE
        )

        for instance in instance_list:
            instance_name = instance.name
            logger.info(f"Deleting instance {instance_name}...")
            self.client.delete(
                project=Settings.GCP_PROJECT_ID,
                zone=Settings.GCP_ZONE,
                instance=instance_name,
            )

        logger.info("All instances have been destroyed.")
