import pandas as pd
from google.cloud import documentai_v1 as documentai

class ReceiptParser:

    def __init__(
            self,
            project_id: str,
            location: str,
            processor_id: str,
            document=None
        ):
        self.project_id = project_id
        self.location = location
        self.project_id = processor_id
        opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}

        # Instantiates a client
        self.documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

        # The full resource name of the processor, e.g.:
        # projects/project-id/locations/location/processor/processor-id
        # You must create new processors in the Cloud Console first
        self.resource_name = self.documentai_client.processor_path(project_id, location, processor_id)
        self.documents = [document] if document else  []

    def parse(
            self,
            file_name: str,
            file_path: str='',
            mime_type: str = "image/png",
        ) -> documentai.Document:
        """
        Processes a document using the Document AI Online Processing API.
        """
        full_file_path = f'{file_path}/{file_name}' if file_path else file_name
        # Read the file into memory
        with open(full_file_path, "rb") as file:
            file_content = file.read()

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(name=self.resource_name, raw_document=raw_document)

        # Use the Document AI client to process the sample form
        result = self.documentai_client.process_document(request=request)
        print("Document processing complete.")
        self.documents.append(result.document)
        
        return result.document
    
    def process(self, document=None, include_metadata=False):
        if document == None:
            document = self.documents[-1] 
        parsed_entities = []
        for entity in getattr(document, 'entities'):
            parsed_entities = self.parse_item(entity, parsed_entities, include_metadata)
            if entity.type_ == 'line_item':
                parsed_properties = {}
                for property in entity.properties:
                    parsed_properties = self.parse_item(property, parsed_properties)
                current_entity = parsed_entities[-1]
                parsed_properties.pop('id')
                parsed_properties.pop('type')
                parsed_properties.pop('mention_text')
                current_entity['type'] = 'line_item'
                for property, value in parsed_properties.items():
                    current_entity[property] = value
        return pd.DataFrame(parsed_entities)
    
    def parse_item(self, entity, parsed_entities, include_metadata=False):
        id = entity.id
        description = entity.type_
        text = entity.mention_text
        value = text
        entity_dict = {
            'id': id,
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
                    field_name = field[0].name
                    value_dict[field_name] = field[1]
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
        if type(parsed_entities) == list:
            parsed_entities.append(entity_dict)
        else:
            parsed_entities = {**parsed_entities, **entity_dict}
            parsed_entities[description] = value

        return parsed_entities
        
if __name__ == "__main__":
    PROJECT_ID = "cool-reality-383300"
    LOCATION = "us"  # Format is 'us' or 'eu'
    PROCESSOR_ID = "fa18104348406151"  # Create processor in Cloud Console

    # The local file in your current working directory
    file_name = "receipt_costco.jpg"
    file_path = ''
    # Refer to https://cloud.google.com/document-ai/docs/processors-list
    # for supported file types
    mime_type = "image/png"
    document = None

    parser = ReceiptParser(
        project_id=PROJECT_ID,
        location=LOCATION,
        processor_id=PROCESSOR_ID,
        document=document
    )


    receipt = parser.parse(
        file_name=file_name,
        file_path=file_path,
        mime_type=mime_type,
    )

    receipt_df = parser.process()
    receipt_df