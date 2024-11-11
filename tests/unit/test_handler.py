import json

import pytest

from src import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": {
            "filename": "receipt_costco.jpg"
        },
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }

@pytest.fixture
def mock_receipt_parser(mocker):
    mock_parser = mocker.patch('src.app.ReceiptParser')
    parser_instance = mock_parser.return_value
    parser_instance.parse.return_value = "mocked_receipt"
    parser_instance.process.return_value = {
        "total_amount": 123.45,
        "date": "2023-01-01",
        "merchant": "Test Store"
    }
    
    return mock_parser

def test_lambda_handler(apigw_event, mock_receipt_parser):
    ret = app.lambda_handler(apigw_event, "")
    data = ret["body"]

    assert ret["statusCode"] == 200
    assert "total_amount" in ret["body"]
    
    # Verify parser was called correctly
    mock_receipt_parser.assert_called_once_with(
        project_id=app.PROJECT_ID,
        location=app.LOCATION,
        processor_id=app.PROCESSOR_ID
    )