import sys
import json
import os
from dotenv import load_dotenv
import openai


# Load environment variables from .env file
load_dotenv()

def lambda_handler(event, context):
    """

    """
    messages = []
    try:
        
        status_code = 200
        api_key = os.environ.get('OPENAI_API_KEY')
        organization_id = os.environ.get('OPENAI_ORGANIZATION')

        openai.api_key = api_key
        openai.organization = organization_id

        messages.append(f"API Key: {api_key is not None}, Organization ID: {organization_id is not None}")

        categories = ["advertising", "allowance on eligible capital property", "bad debts", "business start-up costs", "business tax, fees, licenses and dues",
                      "business-use-of-home expenses", "capital cost allowance", "delivery, freight and express", "fuel costs", "insurance", "interest and bank charges",
                      "legal, accounting and other professional fees", "maintenance and repairs", "management and administration fees", "meals and entertainment",
                      "motor vehicle expenses", "office expenses", "other business expenses", "prepaid expenses", "property taxes", "rent", "salaries, wages and benefits",
                      "supplies", "telephone and utilities", "travel"]
        
        supplier_name = get_value(event.get("supplier_name", {}))
        total_amount = get_value(event.get("total_amount", {}))
        supplier_address = get_value(event.get("supplier_address", {}))
        receipt_date = get_value(event.get("receipt_date", {}))

        line_items = event.get("line_items", [])
        concatenated_items = ", ".join([item.get("mention_text", "") for item in line_items])

        prompt_template = f"""
        You are an assistant trained to classify business expenses based on supplier names, amounts, and receipt data.
        Here are the categories you should use:
        {', '.join(categories)}. If it does not fall into any category, mark it as 'others'.

        Classify the following expense based on the supplier name, total amount, and line items. 
        Only return the selected category as a plain string.

        Example:
        Supplier: "Starbucks" -> meals and entertainment
        Supplier: "Delta Airlines" -> travel
        Supplier: "Staples" -> office expenses

        Now classify the following:
        Supplier: "{supplier_name}"
        Total Amount: "{total_amount}"
        Line Items: "{concatenated_items}"
        Date: "{receipt_date}"
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "user", "content": prompt_template}
            ]
        )

        category = response['choices'][0]['message']['content'].strip()

        result = {
            "supplier_name": supplier_name,
            "total_amount": total_amount,
            "receipt_date": receipt_date,
            "line_items": concatenated_items,
            "supplier_address":supplier_address,
            "category": category
        }
        print(response)
        messages.append(f"{json.dumps(result)}")
        body = result

    except Exception as error:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        message = f'[ERROR] An error occurred on line {lineno} in {filename}: {error}.'
        messages.append(message)
        body = json.dumps(message)
        
        print(f'\nOriginal payload: {event.get("payload")}\n')
        print(message)
        status_code = 500

    return {
        "statusCode": status_code,
        "body": body
    }

def get_value(field, default="N/A"):
    return field.get("normalized_value") or field.get("mention_text") or default
