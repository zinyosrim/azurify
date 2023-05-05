import os
from typing import Protocol
from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.resource import ResourceManagementClient

from azurify.azsecrets import AzSecretKeys


DEFAULT_GROUP_NAME = os.environ.get("AZURE_DEFAULT_GROUP_NAME", None)
DEFAULT_LOCATION = os.environ.get("AZURE_DEFAULT_LOCATION", None)
DEFAULT_OBJECT_ID = os.environ.get("AZURE_DEFAULT_OBJECT_ID", None)


@dataclass
class Secrets:
    secrets: dict()


@dataclass
class Secret:
    key: AzSecretKeys
    value: str


def resource_client(
    group_name: str = DEFAULT_GROUP_NAME, location: str = DEFAULT_LOCATION
) -> ResourceManagementClient:
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ.get("AZURE_SUBSCRIPTION_ID", None),
    )
    resource_client.resource_groups.create_or_update(group_name, {"location": location})
    return resource_client


def keyvault_client() -> KeyVaultManagementClient:
    return KeyVaultManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ.get("AZURE_SUBSCRIPTION_ID", None),
    )


class Tresor(Protocol):
    def create() -> None:
        ...

    def delete() -> None:
        ...


class Keyvault:
    def __init__(
        self,
        tresor_name,
        resource_container=DEFAULT_GROUP_NAME,
        location=DEFAULT_LOCATION,
        keyvault_client=keyvault_client,
    ):
        self.tresor_name = tresor_name
        self.resource_container = resource_container
        self.tenant_id = os.environ.get("AZURE_TENANT_ID", None)
        self.group_name = resource_container
        self.location = location
        self.object_id = DEFAULT_OBJECT_ID
        self.keyvault_client = keyvault_client

    def create(self) -> None:
        self.keyvault_client.vaults.begin_create_or_update(
            self.group_name,
            self.tresor_name,
            {
                "location": self.location,
                "properties": {
                    "tenant_id": self.tenant_id,
                    "sku": {"family": "A", "name": "standard"},
                    "access_policies": [
                        {
                            "tenant_id": self.tenant_id,
                            "object_id": self.object_id,
                            "permissions": {
                                "secrets": [
                                    "get",
                                    "list",
                                    "set",
                                    "delete",
                                    "purge",
                                ],
                            },
                        }
                    ],
                    "enabled_for_deployment": True,
                    "enabled_for_disk_encryption": True,
                    "enabled_for_template_deployment": True,
                },
            },
        ).result()

    @property
    def keyvault(self):
        return self.keyvault_client.vaults.get(self.group_name, self.tresor_name)

    def delete(self) -> None:
        self.keyvault_client.vaults.delete(self.group_name, self.tresor_name)


def main():
    print(f"executing {__name__} in {__file__}")


if __name__ == "__main__":
    main()
