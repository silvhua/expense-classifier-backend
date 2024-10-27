# Expense Classifier Back End (Vancouver Datajam 2024)

The Expense Classifier is a full-stack, serverless application that combines computer vision and language modelling to automate the classification of business expenses from receipts. The application leverages Google's Document AI to extract and parse structured data from receipt images and then uses OpenAI's language model to classify the expenses into relevant predefined business categories. Finally, users can download the classified expenses in CSV format.

## Problem Statement

Businesses and organizations frequently process large volumes of receipts and invoices, often leading to manual, time-consuming tasks such as sorting, classifying, and categorizing expenses. These activities can result in errors, inefficiencies, and a lack of proper insights into business expenditures.

Our application solves this problem by automating the process of extracting data from receipts, classifying the expenses into categories such as "Travel" or "Meals," and providing an easy-to-download CSV file of the classified expenses.

## Architecture

The system architecture consists of:

- **React Frontend**: Users upload receipt images through the React UI and download the resulting CSV file after processing.
- **API Gateway**: Acts as the entry point, forwarding requests from the React frontend to AWS Lambda.
- **AWS Lambda (Parser and Classifier Functions)**: 
  - The first Lambda function sends the uploaded receipt to Google Document AI for parsing.
  - The second Lambda function sends the parsed data to OpenAI for classification and returns the categorized data.
- **Google Document AI**: A pre-built expense parser model that extracts structured data (vendor name, total amount, date, line items) from receipts.
- **OpenAI GPT**: Used for classifying the parsed text data into specific business expense categories (like "Travel," "Meals," or "Office Supplies").
- **CSV Generation**: After classification, the backend generates a CSV file that is sent back to the frontend for the user to download.


## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
expense-classifier-be$ pip install -r tests/requirements.txt --user
# unit test
expense-classifier-be$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
expense-classifier-be$ AWS_SAM_STACK_NAME="expense-classifier-be" python -m pytest tests/integration -v
```
