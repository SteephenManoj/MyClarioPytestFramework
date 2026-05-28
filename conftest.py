import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
from src.resources.utils.excel_utils import get_test_data
from src.resources.utils.logger import LogGenerator

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="session")               # <-- NEW fixture
def logger():
    """Session‑scoped logger – one log file per test run."""
    return LogGenerator.loggen()

@pytest.fixture
def page(browser, request):

    context = browser.new_context()

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    page = context.new_page()

    yield page

    trace_path = Path(f"traces/{request.node.name}.zip")
    trace_path.parent.mkdir(exist_ok=True)

    context.tracing.stop(path=str(trace_path))

    context.close()


def pytest_addoption(parser):
    parser.addini("testdata_file", "Path to Excel test data file", default="src/resources/testdata/TestData.xlsx")
    parser.addini("testdata_sheet", "Sheet name in Excel file", default="Login")


@pytest.fixture(scope="session")
def testdata(request):
    file_path = Path(request.config.getini("testdata_file"))
    sheet_name = request.config.getini("testdata_sheet")

    if not file_path.is_absolute():
        file_path = Path(request.config.rootdir) / file_path

    return get_test_data(file_path, sheet_name)


