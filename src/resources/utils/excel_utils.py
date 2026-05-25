# utils/excel_utils.py
import pandas as pd
from pathlib import Path

TESTDATA_DIR = Path(__file__).resolve().parents[1] / "testdata"

# def read_excel_as_dicts(path, sheet_name='Login'):
#     df = pd.read_excel(Path(path), sheet_name=sheet_name, engine='openpyxl')
#     return df.fillna('').to_dict(orient='records')

def read_excel_as_dicts(path, sheet_name='TestData'):
    try:
        df = pd.read_excel(Path(path), sheet_name=sheet_name, engine='openpyxl')
    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found: {path}")
    except ValueError as e:
        if f"Worksheet named '{sheet_name}' not found" in str(e):
            raise ValueError(f"Sheet '{sheet_name}' not found in {path}")
        raise
    return df.fillna('').to_dict(orient='records')


def get_test_data(file_name, sheet_name='TestData'):
    path = Path(file_name)
    if not path.is_absolute():
        path = TESTDATA_DIR / path
    return read_excel_as_dicts(path, sheet_name=sheet_name)

