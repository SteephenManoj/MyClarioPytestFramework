from pathlib import Path
import pytest

# def get_testdata_path(filename, sheet_name=None):
#     """Get test data path from pytest.ini or use defaults"""
#     # Try to read from pytest.ini
#     config = pytest.Config()
#     testdata_dir = config.getini('testdata_dir')
    
#     if not testdata_dir:
#         testdata_dir = "testdata"  # Default
    
#     path = Path(__file__).parent.parent / testdata_dir / filename
#     return path

def get_testdata_path(pytestconfig, filename):
    testdata_dir = pytestconfig.getini('testdata_dir') or 'testdata'
    return Path(__file__).parent.parent / testdata_dir / filename