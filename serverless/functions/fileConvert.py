from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

endpoint = "your_endpoint"  # From Azure portal
key = "your_key"  # From Azure portal

form_recognizer_client = FormRecognizerClient(endpoint, credential=AzureKeyCredential(key))

with open("path_to_your_pdf_or_image", "rb") as document:
    poller = form_recizer_client.begin_recognize_content(document)
    pages = poller.result()

# Iterate over extracted data
for page in pages:
    print("Page number: {}".format(page.page_number))
    for table in page.tables:
        for cell in table.cells:
            print("Cell text: {}".format(cell.text))
            # Additional processing as needed
