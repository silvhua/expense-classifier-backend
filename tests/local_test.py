import sys
sys.path.append('../src')
print(sys.path)
from app import *
import json

if __name__ == "__main__":
    filepath = '../events/event.json'

    with open(filepath) as file:
        event = json.load(file)
        
    output = lambda_handler(event, None)
