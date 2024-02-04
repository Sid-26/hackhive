import azure.functions as func
import datetime
import json
import logging
import os
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.function_name("RootTrigger")
@app.route(route="hello/{name:alpha}", auth_level=func.AuthLevel.FUNCTION)
def RootTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.route_params.get('name')

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.info("not a json")
        else:
            name = req_body.get('name')


    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
                status_code=200
        )

@app.function_name(name="FileUploadToBlob")
@app.route(route="upload", auth_level=func.AuthLevel.FUNCTION)
def FileUploadToBlob(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(req)
    logging.info("Started upload file process")
    try:
        file = req.files.get('file')
        logging.info(f"Detected {file.filename}")
        
        container = "funny" # os.environ.get("CONTAINER_NAME")
        connection = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1" # os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

        logging.info(f"Connection string: {connection}")

        # implement blob account set up 
        blob_service = BlobServiceClient.from_connection_string(connection)
        blob_client = blob_service.get_blob_client(container=container,blob=file.filename)

        logging.info(f"connected to blob storage with the container name: {container}")

        try:
            logging.info("Uploading file")
            blob_client.upload_blob(file)
        except Exception as e:
            logging.info("File upload failed")
            logging.info(e.args)
        else:
            logging.info("File uploaded successfully")

    except Exception as e:
        logging.info("Something went wrong with file upload")
        logging.info(e.args)
        return func.HttpResponse(body=json.dumps({"fileUploaded":False}), status_code=400)

    return func.HttpResponse(body=json.dumps({"fileUploaded":True}), status_code=201)