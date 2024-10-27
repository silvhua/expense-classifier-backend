# Expense Classifier Back End (Vancouver Datajam 2024)

The Expense Classifier is a full-stack, serverless application that combines computer vision and language modelling to automate the classification of business expenses from receipts. The application leverages Google's Document AI to extract and parse structured data from receipt images and then uses OpenAI's language model to classify the expenses into relevant predefined business categories. Finally, users can download the classified expenses in CSV format.

## Problem Statement

Businesses and organizations frequently process large volumes of receipts and invoices, often leading to manual, time-consuming tasks such as sorting, classifying, and categorizing expenses. These activities can result in errors, inefficiencies, and a lack of proper insights into business expenditures.

Our application solves this problem by automating the process of extracting data from receipts, classifying the expenses into categories such as "Travel" or "Meals," and providing an easy-to-download CSV file of the classified expenses.

## Architecture

The system architecture consists of:

- **React Frontend**: Users upload receipt images through the React UI and download the resulting CSV file after processing.
- **AWS SQS**: For storing the uploaded receipts.
- **AWS Lambda (Parser and Classifier Functions)**: 
  - The first Lambda function sends the uploaded receipt to Google Document AI for parsing.
  - The second Lambda function sends the parsed data to OpenAI for classification and returns the categorized data.
- **Google Document AI**: A pre-built expense parser model that extracts structured data (vendor name, total amount, date, line items) from receipts.
-------------------------------------------------------------------------------------------------------------------------------------
#### Data Split
- ***Train Dataset***: Total 234 receipt
- ***Test Dataset***： Total 46 receipt
  
#### Evaluation Metrics
- ***F1 Score***: 0.813: This score indicates a strong balance between precision and recall for the labeling task. An F1 score above 0.8 is generally considered good, suggesting that the model effectively identifies labels while maintaining accuracy.
- ****F1 score****: the harmonic mean of precision and recall, which combines precision and recall into a single metric, providing equal weight to both. Defined as 2 * (Precision * Recall) / (Precision + Recall)


- ***Precision***: 85.5%: This high precision indicates that when the model labels an instance, it is correct 85.5% of the time. This is important in labeling tasks where false positives can lead to misclassification and impact downstream applications.
- ****Precision****: the proportion of predictions that match the annotations in the test set. Defined as True Positives / (True Positives + False Positives)

- ***Recall***: 77.6%: The recall score indicates that the model correctly identifies 77.6% of all relevant instances (true positives). While this is decent, there is room for improvement, especially if missing relevant labels (false negatives) could significantly affect our use case.
- ****Recall****: the proportion of annotations in the test set that are correctly predicted. Defined as True Positives / (True Positives + False Negatives)
  
#### Evaluation Context
- ***Test Documents***: The model was tested on 39 documents, providing a small but manageable dataset for evaluation.

- ***Evaluated Documents***: All 39 documents were evaluated, showing that there were no issues with the dataset.

- ***Invalid Documents***: With 0 invalid documents, this means all our documents were formatted correctly and usable for the model.

- ***Failed Documents***: 0 failed documents indicates a smooth evaluation process without any errors.

-------------------------------------------------------------------------------------------------------------------------------------
- **OpenAI GPT**: gpt-4o-mini - Used for classifying the parsed text data into specific business expense categories (like "Travel," "Meals," or "Office Supplies").
- **CSV Generation**: After classification, the backend generates a CSV file that is sent back to the frontend for the user to download.




