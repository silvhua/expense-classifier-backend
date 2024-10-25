import sys
import json
from Custom_Logger import *
from ReceiptParser import *
# from openai import OpenAIa


def lambda_handler(event, context):
    """

    """
    messages = []
    try:
        messages.append('hello world')
        status_code = 200
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
    return {
        "statusCode": status_code,
        "body": json.dumps("".join([f"{message}\n" for message in messages])),
    }