# cd model
# python save.py -c '***AZURE_STORAGE_CONNECTION_STRING***'

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import argparse

# https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli

try:
    print("Azure Blob Storage Python quickstart sample")

    parser = argparse.ArgumentParser(description='Upload Model')
    parser.add_argument('-c', '--connection', required=True, help="azure storage connection string")
    args = parser.parse_args()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(args.connection)

    # account_url = "https://affolma.blob.core.windows.net"
    # default_credential = DefaultAzureCredential()
    # Create the BlobServiceClient object
    # blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    exists = False
    containers = blob_service_client.list_containers(include_metadata=True)
    suffix = 0
    for container in containers:
        existingContainerName = container['name']
        print(existingContainerName, container['metadata'])
        if existingContainerName.startswith("climatechange-model"):
            parts = existingContainerName.split("-")
            print(parts)
            if (len(parts) == 3):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    suffix += 1
    container_name = str("climatechange-model-" + str(suffix))
    print("new container name: ")
    print(container_name)

    for container in containers:            
        print("\t" + container['name'])
        if container_name in container['name']:
            print("EXISTIERTT BEREITS!")
            exists = True

    if not exists:
        # Create the container
        container_client = blob_service_client.create_container(container_name)

    # List of model files to upload
    model_files = ["linear_regression_model.pkl", "polynomial_regression_model.pkl", "random_forest_model.pkl"]

    for model_file in model_files:
        local_file_path = os.path.join(".", model_file)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=model_file)
        print(f"\nUploading to Azure Storage as blob:\n\t{model_file}")

        # Upload the created file
        with open(file=local_file_path, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True)

except Exception as ex:
    print('Exception:')
    print(ex)
    exit(1)
