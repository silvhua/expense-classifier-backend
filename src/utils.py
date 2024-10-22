import pandas as pd
import pickle
from datetime import datetime
import json
import boto3

def savepickle(model,filename, ext='sav', path=None,append_version=False):
    """
    Export object as a pickle.
    Parameters:
    - model: Model variable name.
    - filename: Root of the filename.
    - extension: Extension to append (do not include dot as it will be added)
    - filepath (raw string): Use the format r'<path>'. If None, file is saved in same director.
    - append_version (bool): If true, append date and time to end of filename.
    """
    if path:
        path = f'{path}/'.replace('\\','/')
    if append_version == True:
        filename+= f"_{datetime.now().strftime('%Y-%m-%d_%H%M')}"
    full_path = path+filename+'.'+ext if ext else path+filename
    with open (full_path, 'wb') as fh:
        pickle.dump(model, fh)
    print('File saved: ',full_path)
    print('\tTime completed:', datetime.now())

def load_receipt(filename):
    s3 = boto3.client('s3')
    s3_response = s3.get_object(Bucket='datajam-expense-parser', Key=f'receipts/{filename}')
    file_content = s3_response['Body'].read()
    return file_content
    