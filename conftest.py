import pytest
import re
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from pathlib import Path
from src.resources.utils.excel_utils import get_test_data
from src.resources.utils.logger import LogGenerator

try:
    import allure
except ImportError:
    allure = None

# ===== Generate Timestamped Report Directory =====
def _get_test_suite_name():
    """Extract test suite name from command line arguments or environment"""
    # Default to the first test file name or 'general'
    test_files = []
    for arg in pytest.config.args if hasattr(pytest, 'config') else []:
        if arg.endswith('.py'):
            suite_name = Path(arg).stem
            return suite_name
    return 'general'

def pytest_configure(config):
    """Create timestamped report directories before test run"""
    # Get current timestamp in format: YYYY-MM-DD_HH-MM-SS
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Try to determine test suite name from collected tests
    suite_name = "general"
    if hasattr(config, 'invocation_params') and config.invocation_params.args:
        for arg in config.invocation_params.args:
            if 'test_' in arg and arg.endswith('.py'):
                suite_name = Path(arg).stem.replace('test_', '')
                break
    
    # Create timestamped report directory
    report_base = Path(config.rootpath) / "reports"
    report_dir = report_base / f"{timestamp}_{suite_name}"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Store report paths in config for access in other hooks
    config.report_dir = report_dir
    config.allure_dir = report_dir / "allure-results"
    config.html_report = report_dir / "report.html"
    config.logs_dir = report_dir / "logs"
    
    # Create subdirectories
    config.allure_dir.mkdir(parents=True, exist_ok=True)
    config.logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Update pytest options dynamically
    config.option.allure_report_dir = str(config.allure_dir)
    config.option.htmlpath = str(config.html_report)
    
    # Add plugin options for html and allure
    config.addinivalue_line("addopts", f"--alluredir={config.allure_dir} --html={config.html_report}")


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=2000, args=["--start-maximized"]) 
        yield browser
        browser.close()

@pytest.fixture(scope="session")               # <-- NEW fixture
def logger(request):
    """Session‑scoped logger – one log file per test run."""
    log_file = Path(request.config.logs_dir) / "test_execution.log"
    return LogGenerator.loggen(log_file=str(log_file))

@pytest.fixture
def page(browser, request):

    context = browser.new_context(no_viewport=True)
    
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    page = context.new_page()
    yield page

    # Store traces in timestamped directory
    traces_dir = Path(request.config.rootpath) / "traces" / datetime.now().strftime("%Y-%m-%d")
    trace_path = traces_dir / f"{request.node.name}.zip"
    trace_path.parent.mkdir(parents=True, exist_ok=True)

    context.tracing.stop(path=str(trace_path))

    context.close()


def _safe_file_name(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")


def _capture_step_screenshot(request, scenario, step, step_func_args, status):
    page = step_func_args.get("page")
    if page is None:
        return

    # Use timestamped report directory for screenshots
    screenshot_dir = Path(request.config.report_dir) / "screenshots" / status
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    scenario_name = _safe_file_name(scenario.name)
    step_name = _safe_file_name(step.name)
    # Include test case ID if available
    test_id = getattr(request.node, 'callspec', None)
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


def pytest_sessionfinish(session, exitstatus):
    """Generate Allure HTML report after test session ends"""
    if not allure:
        return
    
    report_dir = Path(session.config.report_dir)
    allure_dir = report_dir / "allure-results"
    allure_html_dir = report_dir / "allure-report"
    
    # Only generate if allure-results exist
    if not allure_dir.exists() or not list(allure_dir.glob("*.json")):
        return
    
    try:
        import subprocess
        # Generate Allure HTML report
        result = subprocess.run(
            ["allure", "generate", str(allure_dir), "-o", str(allure_html_dir), "--clean"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ Allure HTML report generated: {allure_html_dir / 'index.html'}")
        else:
            print(f"\n⚠ Allure report generation failed: {result.stderr}")
            print("  Install Allure CLI: https://docs.qameta.io/allure/#_installing_a_commandline")
    except FileNotFoundError:
        print("\n⚠ Allure CLI not found. Install it with: 'pip install allure-pytest'")
        print("  Then install Allure commandline tool from: https://docs.qameta.io/allure/#_installing_a_commandline")


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

