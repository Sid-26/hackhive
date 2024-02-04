import function_app
import json
import csv
import xml.etree.ElementTree as ET
from azure.storage.blob import BlobServiceClient

#main download function
def downloadBlobAsString(blobServiceClient, containerName, blobName):
    blobClient = blobServiceClient.get_blob_client(container = containerName, blob = blobName)
    blobData = blobClient.download_blob().readall()
    return blobData.decode('utf-8')

#json converter
def jsonToCsv(json, csvFilePath):
    with open(csvFilePath, 'w', newline = '') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = json[0].keys())
        writer.writeheader()

        for row in json:
            writer.writerow(row)

#xml converter
def xmlToCsv(xmlData, csvFilePath):
    root = ET.fromstring(xmlData)
    rows = []

    for child in root:
        row_data = {elem.tag: elem.text for elem in child}
        rows.append(row_data)

    if rows:
        with open(csvFilePath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

#blob download processing
def processBlob(blobServiceClient, containerName, blobName, outputPath):
    
    #check file type, and convert accordingly
    fileExt = blobName.split('.')[-1].lower()

    if fileExt in ['json', 'xml']:
        #download the file as string
        fileContent = downloadBlobAsString(blobServiceClient, containerName, blobName)

        if fileExt == 'json':
            #convert json to csv
            json_data = json.loads(fileContent)
            jsonToCsv(json_data, outputPath)

        elif fileExt == 'xml':
            #convert xml to csv
            xmlToCsv(fileContent, outputPath)
        
        print(f"Converted {blobName} to CSV at {outputPath}")

    elif fileExt == 'csv':
        #download csv directly
        blobClient = blobServiceClient.get_blob_client(container = containerName, blob = blobName)
        
        with open(outputPath, "wb") as download_file:
            download_file.write(blobClient.download_blob().readall())
        print(f"Downloaded {blobName} to {outputPath}")

    else:
        print("Unsupported file format, please use .CSV, .XML or .JSON")

#blob details
connectionString = "need input"
containerName = "need input"
blobFileName = "blob name here with extension"  # e.g., "data.json"

#initalize blob client
blobServiceClient = BlobServiceClient.from_connection_string(connectionString)

# Process the Blob based on its type
outputFilePath = "output.csv"
processBlob(blobServiceClient, containerName, blobFileName, outputFilePath)