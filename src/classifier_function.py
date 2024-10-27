import sys
import json
import os
from dotenv import load_dotenv
import openai
# from Custom_Logger import *
# from ReceiptParser import *
# from openai import openai_client

# Load environment variables from .env file
load_dotenv()
openai.api_key = "sk-svcacct-kZ9qEr5giEFAMJERoO8sErMgjIagL8Xm1bsettbHRI3rUh8v2PxPYT2xDL0PVrbjalIT3BlbkFJBhmhobLbS9oltClDFAxnaHpmrxcUMK_kI_2JJEMW8oypOObSz9KB3BjjjdCxTf3h6qgA"
openai.organization = "org-PpIzKg3IAEo6MJkkbHxIVaFz"

def lambda_handler(event, context):
    """

    """
    messages = []
    try:
        
        status_code = 200

        # api_key = os.getenv('OPENAI_API_KEY')
        # org_id = os.getenv('OPENAI_ORGANIZATION')
        # messages.append(f"API Key: {api_key is not None}, Organization ID: {org_id is not None}")

        # Define categories
        categories = ["advertising", "allowance on eligible capital property", "bad debts", "business start-up costs", "business tax, fees, licenses and dues",
                      "business-use-of-home expenses", "capital cost allowance", "delivery, freight and express", "fuel costs", "insurance", "interest and bank charges",
                      "legal, accounting and other professional fees", "maintenance and repairs", "management and administration fees", "meals and entertainment",
                      "motor vehicle expenses", "office expenses", "other business expenses", "prepaid expenses", "property taxes", "rent", "salaries, wages and benefits",
                      "supplies", "telephone and utilities", "travel"]

        # Extract line items from parsed receipt
        item = event.get("supplier_name")

        # Extract additional information
        total_amount = event.get("total_amount", {}).get("normalized_value")
        supplier_address = event.get("supplier_address", {}).get("normalized_value", "N/A")
        receipt_date = event.get("receipt_date", {}).get("normalized_value", "N/A")
        supplier_city = event.get("supplier_city", {}).get("normalized_value", "N/A")

        # Format the prompt for classification
        prompt_template = f"""
        You are an assistant trained to classify business expenses from receipt data. Here are the categories you should use:
        {', '.join(categories)}.

        Classify the supplier based on the description provided. Return the classification in JSON format:
        {{ 
            "supplier name": "item", 
            "category": "selected category",
            "total_amount": "{total_amount}",
            "supplier_address": "{supplier_address}",
            "receipt_date": "{receipt_date}",
            "supplier_city": "{supplier_city}"
        }}.

        Example:
        Items:
        - "Large Coffee" - meals and entertainment
        - "Notebook" - office expenses
        - "Train Ticket to Downtown" - travel
        - "Grocery" - supplies

        Now classify the following items:
        {item}
        """
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Replace with your preferred model
            messages=[
                {"role": "user", "content": prompt_template}
            ]
        )
        
        # Extract and handle the structured output
        structured_output = response.choices[0].message['content']

        # Debugging: print the raw output
        # print("Structured Output:", structured_output)

        # # Attempt to parse the structured output as JSON
        # classification_result = json.loads(structured_output)

        # # Create final output JSON
        # final_output = {
        #     "supplier_name": item,
        #     "category": classification_result.get("category"),
        #     "total_amount": event.get("total_amount", {}).get("normalized_value", "N/A"),
        #     "supplier_address": event.get("supplier_address", {}).get("normalized_value", "N/A"),
        #     "receipt_date": event.get("receipt_date", {}).get("normalized_value", "N/A"),
        #     "supplier_city": event.get("supplier_city", {}).get("normalized_value", "N/A")
        # }
        # messages.append(json.dumps(final_output, indent=4))

        messages.append(f"{structured_output}")

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
        "body": messages
    }