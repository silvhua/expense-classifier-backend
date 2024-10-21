import sys
import json
from Custom_Logger import *
# from ReceiptParser import *
# from openai import OpenAI


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
    message = ''
    try:
        if type(event.get('body')) == str:
            payload = json.loads(event["body"])
        else:
            payload = event.get('body')
        name = payload.get('name')
        message = f'Hello there, {name}!'
        local_invoke = event.get('direct_local_invoke', None)
        logging_level = logging.DEBUG if local_invoke else logging.INFO
        logger = Custom_Logger(__name__, level=logging_level)
        logger.info(f'Payload: {payload}\nLocal invoke: {local_invoke}')
    except Exception as error:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        message += f'[ERROR] An error occurred on line {lineno} in {filename}: {error}.'
        
        print(f'\nOriginal payload: {event.get("payload")}\n')
        print(message)
    return {
        "statusCode": 200,
        "body": json.dumps(message),
    }
