from azure.storage.blob import BlobServiceClient

def blobDownload(storageAccountName, storageAccountKey, containerName, blobName, destinationPath):
    try:
        #create blob service clint
        blobServiceClient = BlobServiceClient(account_url = f"https://{storageAccountName}.blob.core.windows.net", credential = storageAccountKey)

        #get a blob client using the container and blob name
        blobClient = blobServiceClient.get_blob_client(container = containerName, blob = blobName)

        #download the blob content
        with open(destinationPath, "wb") as download_file:
            download_file.write(blobClient.download_blob().readall())

        print(f"Blob '{blobName}' downloaded to '{destinationPath}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

#testing (needs blob account info)
storageAccountName = ''
storageAccountKey = ''
containerName = ''
blobName = ''
destinationPath = ''

blobDownload(storageAccountName, storageAccountKey, containerName, blobName, destinationPath)
