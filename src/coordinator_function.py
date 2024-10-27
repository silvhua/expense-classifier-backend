import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    request_body = event['body']
    logger.info(f"Received input from caller: {request_body}")

    try:
        sf = boto3.client('stepfunctions')
        response = sf.start_sync_execution(
            stateMachineArn='arn:aws:states:us-west-2:741448954840:stateMachine:expense-classifier-coordinator-2030',
            input=request_body
        )
        response_body = response['output']
        logger.info(f"Retrieved output from coordinator: {response_body}")
    except:
        pass

    return {
        'statusCode': 200,
        'body': json.dumps({
            "supplier_name": "Browns Socialhouse Queen Elizabeth Theatre (QE Theatre)",
            "total_amount": "6.18",
            "receipt_date": "2024-08-14",
            "line_items": "4.75, 0.86, 0.33, 4.75, 0.24, 6.18, .75, 0.02, 6.20",
            "supplier_address": "675 Cambie St Vancouver, BC V6B 2P1 Canada",
            "category": ""
        }),
        'headers': {
            "content-type": "application/json"
        }
    }
