import pandas as pd
import pickle
from datetime import datetime

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