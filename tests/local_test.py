import sys
sys.path.append('../src')
from app import *
import json

if __name__ == "__main__":
    filepath = '../events/event.json'

    with open(filepath) as file:
        event = json.load(file)
        
    df = lambda_handler(event, None)