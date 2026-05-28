import pytest
import re
import os
from playwright.sync_api import sync_playwright
from pathlib import Path
from src.resources.utils.excel_utils import get_test_data
from src.resources.utils.logger import LogGenerator
 
try:
    import allure
except ImportError:
    allure = None
 

def _load_env_file():
    project_root = Path(__file__).parent
    env_paths = [
        project_root / "envs" / ".env",
        project_root / ".env",
    ]
    env_path = next((path for path in env_paths if path.exists()), None)

    if env_path is None:
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser_name = os.getenv("MYCLARIO_BROWSER", "chromium").lower()
        headless = os.getenv("MYCLARIO_HEADLESS", "false").lower() in ("1", "true", "yes")
        browser_type = getattr(playwright, browser_name)
        browser = browser_type.launch(headless=headless)
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
 
 
def _safe_file_name(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
 
 
def _capture_step_screenshot(request, scenario, step, step_func_args, status):
    page = step_func_args.get("page")
    if page is None:
        return
 
    screenshot_dir = Path(request.config.rootpath) / "reports" / "screenshots" / status
    screenshot_dir.mkdir(parents=True, exist_ok=True)
 
    scenario_name = _safe_file_name(scenario.name)
    step_name = _safe_file_name(step.name)
    screenshot_path = screenshot_dir / f"{scenario_name}_{step_name}.png"
 
    page.screenshot(path=str(screenshot_path), full_page=True)
 
    if allure:
        allure.attach.file(
            str(screenshot_path),
            name=f"{status.upper()} - {step.name}",
            attachment_type=allure.attachment_type.PNG,
        )
 
 
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    _capture_step_screenshot(request, scenario, step, step_func_args, "passed")
 
 
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    _capture_step_screenshot(request, scenario, step, step_func_args, "failed")
 
 
def pytest_addoption(parser):
    parser.addini("testdata_file", "Path to Excel test data file", default="src/resources/testdata/TestData.xlsx")
    parser.addini("testdata_sheet", "Sheet name in Excel file", default="Login")
 
 
@pytest.fixture(scope="session")
def testdata(request):
    file_path = Path(os.getenv("MYCLARIO_TESTDATA_FILE", request.config.getini("testdata_file")))
    sheet_name = os.getenv("MYCLARIO_TESTDATA_SHEET", request.config.getini("testdata_sheet"))
 
    if not file_path.is_absolute():
        file_path = Path(request.config.rootdir) / file_path
 
    return get_test_data(file_path, sheet_name)
 
 
# # Login Test Data
# @pytest.fixture(scope="session")
# def login_data():
#     return get_test_data(
#         "TestData.xlsx",
#         "Login"
#     )
 
 
# # Register Test Data
# @pytest.fixture(scope="session")
# def register_data():
#     return get_test_data(
#         "TestData.xlsx",
#         "Register"
#     )
 
 
 
