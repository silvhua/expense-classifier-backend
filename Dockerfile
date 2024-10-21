# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-base
# Python 3.12 did not work
FROM public.ecr.aws/lambda/python:3.10  

ARG GOOGLE_APPLICATION_CREDENTIALS_PATH

# Copy requirements.txt
COPY ./src/requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
# `yum install gcc -y` is to avoid issue with building `bottleneck` wheel when running Docker image locally
RUN yum install gcc -y
RUN python -m pip install --upgrade pip setuptools
RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# set environment variables
# ENV GOOGLE_APPLICATION_CREDENTIALS=${LAMBDA_TASK_ROOT}/clientLibraryConfig-0000.json
# ENV GOOGLE_APPLICATION_CREDENTIALS=${LAMBDA_TASK_ROOT}/application_default_credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS_PATH}

# Copy function code
COPY ./src/* ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]