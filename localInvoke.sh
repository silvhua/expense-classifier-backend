# https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
# https://github.com/aws/aws-lambda-runtime-interface-emulator?tab=readme-ov-file#test-an-image-with-rie-included-in-the-image

docker kill $(docker ps -aq)
docker build -t local . 
docker run -d -p 9000:8080 local:latest
curl -X POST -H "Content-Type: application/json" -d "@events/event.json" http://localhost:9000/2015-03-31/functions/function/invocations