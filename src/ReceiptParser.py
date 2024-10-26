import pandas as pd
from google.cloud import documentai_v1 as documentai
import os
from typing import Optional
from utils import savepickle, load_receipt
import json

class ReceiptParser:

    def __init__(
            self,
            project_id: str,
            location: str,
            processor_id: str
        ):
        self.project_id = project_id
        self.location = location
        self.project_id = processor_id
        self.entities_to_parse = ['line_item', 'total_amount', 'supplier_name', 'supplier_address', 'receipt_date', 'supplier_city']
        # api_key_string = os.environ.get('GOOGLE_API_KEY')
        opts = {
            "api_endpoint": f"{location}-documentai.googleapis.com",
            # "api_key": api_key_string
            }

        # Instantiates a client
        self.documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

        # The full resource name of the processor, e.g.:
        # projects/project-id/locations/location/processor/processor-id
        # You must create new processors in the Cloud Console first

        self.resource_name = self.documentai_client.processor_path(
            project_id, location, processor_id,
            # client_options={}
            )
        self.documents = {}
        self.dataframes = {}
        self.mime_types = {
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'bmp': 'image/bmp',
            'tiff': 'image/tiff',
        }

    def parse_folder(
            self,
            folder_path: str,
            save_path: Optional[str] = None
        ) -> list[documentai.Document]:
        """
        Processes all files in a folder using the Document AI Online Processing API.
        """
        dataframes = []

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                split_file_name = os.path.splitext(file_name)
                file_ext = split_file_name[1][1:].lower()
                file_name_name = split_file_name[0]
                mime_type = self.mime_types.get(file_ext, 'application/octet-stream')
                document = self.parse(
                    file_name=file_name,
                    file_path=folder_path,
                    mime_type=mime_type,
                    save_path=save_path
                )
                self.documents[file_name_name] = document
                df = self.process(file_name_name)
                dataframes.append(df)
                    
        return dataframes

    def parse(
            self,
            file_name: str,
            file_path: str='',
            s3: Optional[bool] = False,
            save_path: Optional[str] = None
        ) -> documentai.Document:
        """
        Processes a document using the Document AI Online Processing API.
        Refer to https://cloud.google.com/document-ai/docs/processors-list for supported file types

        Parameters:
        - file_name (str): The name of the file to process.
        - file_path (str): The path to the file to process.
        - s3 (bool; optional): Whether or not the file is stored in an S3 bucket.
        - save_path (str; optional): The path to save the processed document.
        """
        full_file_path = f'{file_path}/{file_name}' if file_path else file_name
        # Read the file into memory
        if s3:
            file_content = load_receipt(file_name)
        else:
            with open(full_file_path, "rb") as file:
                file_content = file.read()

        # Load Binary Data into Document AI RawDocument Object
        split_file_name = os.path.splitext(full_file_path)
        file_ext = split_file_name[1][1:].lower()
        file_name_name = split_file_name[0]
        mime_type = self.mime_types.get(file_ext, 'application/octet-stream')
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(name=self.resource_name, raw_document=raw_document)

        # Use the Document AI client to process the sample form
        result = self.documentai_client.process_document(request=request)
        print("Document processing complete.")
        self.documents[file_name_name] = result.document
        if save_path:
            savepickle(
                result.document, file_name_name, path=save_path
            )
        return result.document
    
    def process(self, document_key=None, include_metadata=False):
        if document_key:
            document = self.documents[document_key]
        else:
            first_key = next(iter(self.documents))
            document = self.documents.get(first_key)
            document_key = first_key
        parsed_entities = {}
        parsed_entities['line_items'] = []
        for entity in getattr(document, 'entities'):
            entity_type = entity.type_
            if entity_type in self.entities_to_parse:
                parsed_entity = self.parse_item(entity, include_metadata)
                if entity.type_ == 'line_item':
                    parsed_properties = {}
                    for property in entity.properties:
                        parsed_properties = self.parse_item(property, parsed_properties)
                    current_entity = parsed_entity
                    parsed_properties.pop('id')
                    
                    current_entity['type'] = entity_type
                    for property, value in parsed_properties.items():
                        current_entity[property] = value
                    parsed_entities['line_items'].append(current_entity)
                else:
                    parsed_entities[entity_type] = parsed_entity
        return parsed_entities
    
    def parse_item(self, entity, include_metadata=False):
        id = entity.id
        description = entity.type_
        text = entity.mention_text
        value = text
        entity_dict = {
            'id': id,
            'mention_text': text,
            'type': description,
            'mention_text': text
        }
        value_type = vars(entity.normalized_value)['_pb'].WhichOneof('structured_value')
        if value_type:
            value = getattr(entity.normalized_value, value_type)
            value_fields = getattr(entity.normalized_value, value_type).ListFields()
            if len(value_fields) > 0:
                value_dict = {}
                for field in value_fields:
                    field_name = field[0].name # field name
                    field_value = field[1] #value
                    #  Ensure it is JSON serializable  because some values will be of type `RepeatedScalarContainer` which is not JSON serializable
                    try: 
                        json.dumps(field_value)
                        value_dict[field_name] = field_value
                    except:
                        try:
                            value_dict[field_name] = field_value[0]
                        except:
                            value_dict[field_name] = ''
                entity_dict = {**entity_dict, **value_dict}
        if entity.normalized_value:
            value = getattr(entity.normalized_value, 'text')
            entity_dict['normalized_value'] = value.strip()
            
        if include_metadata:
            confidence = f"{entity.confidence:.0%}"

            # entity.page_ref contains the pages that match the classification
            pages_list = []
            for page_ref in entity.page_anchor.page_refs:
                pages_list.append(page_ref.page)
            pages = pages_list

            entity_dict['confidence'] = confidence
            entity_dict['pages'] = pages
        return entity_dict
        
if __name__ == "__main__":
    PROJECT_ID = "datajam-438419"
    LOCATION = "us"  # Format is 'us' or 'eu'
    PROCESSOR_ID = "e781102d22fb3b53"  # Create processor in Cloud Console

    # The local file in your current working directory
    file_name = "2019-07-04 staples printing receipt.pdf"
    file_path = './data/receipts/2024-10-19'
    # Refer to https://cloud.google.com/document-ai/docs/processors-list
    # for supported file types

    parser = ReceiptParser(
        project_id=PROJECT_ID,
        location=LOCATION,
        processor_id=PROCESSOR_ID
    ) 

    ### Parse a folder
    # receipts = parser.parse_folder(
    #     folder_path=file_path,
    #     save_path='../data/pickles'
    # )

    ## Parse a single file
    receipt = parser.parse(
        file_name=file_name,
        file_path=file_path,
    )
    receipt_df = parser.process()
    print(receipt_df)