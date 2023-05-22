from strenum import StrEnum
from os import environ

class AzEnv(StrEnum):
    AZURE_SUBSCRIPTION_ID = environ['AZURE_SUBSCRIPTION_ID'] 
    AZURE_TENANT_ID = environ['AZURE_TENANT_ID'] 
    AZURE_CLIENT_ID = environ['AZURE_CLIENT_ID'] 
    AZURE_CLIENT_SECRET = environ['AZURE_CLIENT_SECRET'] 
    AZURE_DEFAULT_GROUP_NAME = environ['AZURE_DEFAULT_GROUP_NAME'] 
    AZURE_DEFAULT_LOCATION = environ['AZURE_DEFAULT_LOCATION'] 
    AZURE_DEFAULT_OBJECT_ID = environ['AZURE_DEFAULT_OBJECT_ID'] 

def main():
    print(f"Tenant ID = {AzEnv.AZURE_TENANT_ID}")

if __name__ == "__main__":
    main()