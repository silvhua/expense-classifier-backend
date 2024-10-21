aws lambda update-function-code \
           --function-name arn:aws:lambda:us-west-2:741448954840:function:datajam-prod-ParserFunction-hELUOfmyOAbk \
           --image-uri 741448954840.dkr.ecr.us-west-2.amazonaws.com/docker-lambda-datajam:latest \
           --profile ${AWS_PROFILE} 