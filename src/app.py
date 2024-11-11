import sys
sys.path.append('./src')
import json
from Custom_Logger import *
from ReceiptParser import *
# from openai import OpenAIa



PROJECT_ID = "362542744058"
LOCATION = "us"  # Format is 'us' or 'eu'
PROCESSOR_ID = "e781102d22fb3b53"  # Create processor in Cloud Console

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    messages = []
    try:
        if type(event.get('body')) == str:
            payload = json.loads(event["body"])
        else:
            payload = event.get('body')
    
        message = f'Last update: 2024-11-10 23:54'
        messages.append(message)
        local_invoke = event.get('direct_local_invoke', None)
        if local_invoke:
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO
        logger = Custom_Logger(__name__, level=logging_level)
        logger.info(f'Payload: {payload}\nLocal invoke: {local_invoke}')

        if payload.get('local_file', False) == True:
            # The local file in your current working directory
            file_path = ''
            file_name = 'receipt_browns.jpg'
            use_s3 = False
        else:
            file_name = payload.get('filename', None)
            use_s3 = True
            file_path = ''
        print(f'file_name and path: {file_path}/{file_name}')
        if file_name == None:
            status_code = 500
            messages.append('No image file name provided.')
            return {
                "statusCode": status_code,
                "body": json.dumps("".join([f"{message}\n" for message in messages])),
            }

        parser = ReceiptParser(
            project_id=PROJECT_ID,
            location=LOCATION,
            processor_id=PROCESSOR_ID
        ) 

        ## Parse a single file
        receipt = parser.parse(
            file_name=file_name,
            file_path=file_path,
            s3=use_s3
        )
        receipt_json = parser.process()
        messages.append(f'Receipt parsed successfully.')
        if local_invoke and os.environ.get('DOCKER_INVOKE', 0) == 0:
            return parser
        status_code = 200
        body = receipt_json
        logger.info("".join([f"{message}\n" for message in messages]))
    except Exception as error:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        message = f'[ERROR] An error occurred on line {lineno} in {filename}: {error}.'
        messages.append(message)
        
        print(f'\nOriginal payload: {event.get("payload")}\n')
        print(message)
        status_code = 500
        body = json.dumps("".join([f"{message}\n" for message in messages]))
    logger.info(body)
    return {
        "statusCode": status_code,
        "body": body,
    }