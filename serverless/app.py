from flask import Flask, request, send_from_directory
from flask_cors import CORS
import json
import logging
from azure.storage.blob import BlobServiceClient
import csv
# import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return json.dumps({'statusCode':200,'body':'Hello World!'})

@app.route('/upload', methods=['POST'])
def upload():
    container = "funny"  #os.environ.get("CONTAINER_NAME")
    connection = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1"  #os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    try:
        file = request.files['file']# req.files.get('file')
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
        return json.dumps({'statusCode':400,'body':{'success':False}})
    
    else:
        return json.dumps({'statusCode':200,'body':{'success':True}})
    
@app.route('/clown', methods=['GET'])
def funny():
    with open('app_test_data_comp.csv') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        jay = json.dumps(rows)
        return json.dumps({'statusCode':200,'body':jay})

if __name__ == "__main__":
    app.run()