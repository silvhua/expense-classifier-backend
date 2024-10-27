import sys
sys.path.append('../src')
from classifier_function import *
import json

if __name__ == "__main__":
    filepath = '../events/receipt_costco.json'

    with open(filepath) as file:
        event = json.load(file)
        
    output = lambda_handler(event, None)
    
    # Extract status code
    print("Status Code:", output["statusCode"])

    # Extract and clean up the message
    messages = output.get("body", [])
    print("Messages:")

    for message in messages:
        # Remove markdown formatting
        cleaned_message = message.replace("```json\n", "").replace("\n```", "")
        
        # Convert cleaned message to JSON and pretty print
        message_dict = json.loads(cleaned_message)
        print(json.dumps(message_dict, indent=4))
