# utils/excel_utils.py
import pandas as pd
from pathlib import Path

def read_excel_as_dicts(path, sheet_name='Login'):
    df = pd.read_excel(Path(path), sheet_name=sheet_name, engine='openpyxl')
    return df.fillna('').to_dict(orient='records')