import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
from utils.excel_utils import read_excel_as_dicts

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser, request):
    # Create a new context with tracing enabled
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    # Create a page from the context
    page = context.new_page()
    
    yield page
    
    # After test finishes, stop tracing and save the trace
    trace_path = Path(f"traces/{request.node.name}.zip")
    trace_path.parent.mkdir(exist_ok=True)
    context.tracing.stop(path=str(trace_path))
    context.close()

# @pytest.fixture(scope='session')
# def testdata():
#     p = Path(__file__).parent / "testdata" / "TestData.xlsx"
#     return read_excel_as_dicts(p)

def pytest_addoption(parser):
    """Register custom command-line and ini options."""
    # Register the ini options
    parser.addini("testdata_file", "Path to Excel test data file", default="testdata/TestData.xlsx")
    parser.addini("testdata_sheet", "Sheet name in Excel file", default="TestData")
    
    # Register command-line options that override ini settings
    parser.addoption("--testdata-file", action="store", default=None,
                     help="Override testdata file path")
    parser.addoption("--testdata-sheet", action="store", default=None,
                     help="Override sheet name")  
      
@pytest.fixture(scope='session')
def testdata(request):
    # 1. Try command line option
    file_path = request.config.getoption("--testdata-file")
    sheet_name = request.config.getoption("--testdata-sheet")
    
    # 2. If not provided, fall back to pytest.ini settings
    if file_path is None:
        file_path = request.config.getini("testdata_file")
    if sheet_name is None:
        sheet_name = request.config.getini("testdata_sheet")
    
    # 3. Final fallback (optional)
    if file_path is None:
        file_path = "testdata/TestData.xlsx"
    if sheet_name is None:
        sheet_name = "TestData"
    
    # Resolve absolute path relative to pytest rootdir
    rootdir = Path(request.config.rootdir)
    abs_path = rootdir / file_path
    
    if not abs_path.exists():
        raise FileNotFoundError(f"Test data file not found: {abs_path}")
    
    return read_excel_as_dicts(abs_path, sheet_name=sheet_name)