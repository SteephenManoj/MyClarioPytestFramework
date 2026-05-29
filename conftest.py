import pytest
import re
import subprocess
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from src.resources.utils.excel_utils import get_test_data
from src.resources.utils.logger import LogGenerator
 
try:
    import allure
except ImportError:
    allure = None
 
# def pytest_configure(config):
 
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
 
#     report_base = Path(config.rootpath) / "reports"
#     report_dir = report_base / timestamp
 
#     report_dir.mkdir(parents=True, exist_ok=True)
 
#     config.report_dir = report_dir
#     config.allure_dir = report_dir / "allure-results"
#     config.html_report = report_dir / "report.html"
#     config.logs_dir = report_dir / "logs"
 
#     config.allure_dir.mkdir(parents=True, exist_ok=True)
#     config.logs_dir.mkdir(parents=True, exist_ok=True)
 
#     config.option.allure_report_dir = str(config.allure_dir)
#     config.option.htmlpath = str(config.html_report)
 
def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    suite_names = []
    marker_name = "general"
    # Detect marker from command
    if hasattr(config, 'invocation_params'):
        args = config.invocation_params.args
        if "-m" in args:
            marker_index = args.index("-m") + 1
            if marker_index < len(args):
                marker_name = args[marker_index]
        for arg in args:
            if arg.endswith(".py") and "test_" in arg:
                suite_names.append(
                    Path(arg).stem.replace("test_", "")
                )
    # Determine suite name
    if len(suite_names) == 1:
 
        suite_name = suite_names[0]
    elif len(suite_names) > 1:
 
        suite_name = "RegressionSuite"
    else:
 
        suite_name = "FullSuite"
    # Create report path
    report_base = (
        Path(config.rootpath)
        / "reports"
        / marker_name
    )
    report_dir = report_base / f"{timestamp}_{suite_name}"
    report_dir.mkdir(parents=True, exist_ok=True)
    config.report_dir = report_dir
    config.allure_dir = report_dir / "allure-results"
    config.html_report = report_dir / "report.html"
    config.logs_dir = report_dir / "logs"
    config.allure_dir.mkdir(parents=True, exist_ok=True)
    config.logs_dir.mkdir(parents=True, exist_ok=True)
    config.option.allure_report_dir = str(config.allure_dir)
    config.option.htmlpath = str(config.html_report)
 
@pytest.fixture(scope="session")
def browser():
 
    with sync_playwright() as playwright:
 
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=2000,
            args=["--start-maximized"]
        )
 
        yield browser
 
        browser.close()
 
@pytest.fixture(scope="session")
def logger(request):
 
    log_file = Path(request.config.logs_dir) / "execution.log"
 
    return LogGenerator.loggen(log_file=str(log_file))
 
 
@pytest.fixture
def page(browser, request):
 
    context = browser.new_context(
        no_viewport=True
    )
 
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
 
    page = context.new_page()
 
    yield page
 
    trace_dir = Path("traces")
    trace_dir.mkdir(exist_ok=True)
 
    trace_path = trace_dir / f"{request.node.name}.zip"
 
    context.tracing.stop(path=str(trace_path))
 
    context.close()
 
def _safe_file_name(value):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
 
 
def _capture_step_screenshot(request, scenario, step, step_func_args, status):
 
    page = step_func_args.get("page")
 
    if page is None:
        return
 
    screenshot_dir = (
        Path(request.config.report_dir)
        / "screenshots"
        / status
    )
 
    screenshot_dir.mkdir(parents=True, exist_ok=True)
 
    scenario_name = _safe_file_name(scenario.name)
    step_name = _safe_file_name(step.name)
 
    screenshot_path = screenshot_dir / f"{scenario_name}_{step_name}.png"
 
    page.screenshot(
        path=str(screenshot_path),
        full_page=True
    )
 
    if allure:
 
        allure.attach.file(
            str(screenshot_path),
            name=f"{status.upper()} - {step.name}",
            attachment_type=allure.attachment_type.PNG
        )
 
def pytest_bdd_after_step(
    request,
    feature,
    scenario,
    step,
    step_func,
    step_func_args
):
 
    _capture_step_screenshot(
        request,
        scenario,
        step,
        step_func_args,
        "passed"
    )
 
 
def pytest_bdd_step_error(
    request,
    feature,
    scenario,
    step,
    step_func,
    step_func_args,
    exception
):
 
    _capture_step_screenshot(
        request,
        scenario,
        step,
        step_func_args,
        "failed"
    )
 
 
def pytest_sessionfinish(session, exitstatus):
 
    if not allure:
        return
 
    allure_dir = session.config.allure_dir
    allure_report_dir = session.config.report_dir / "allure-report"
 
    try:
        allure_command = "allure"
 
        result = subprocess.run(f'{allure_command} generate "{allure_dir}" -o "{allure_report_dir}" --clean',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
 
            print(
                f"\n✓ Allure report generated successfully:\n"
                f"{allure_report_dir / 'index.html'}"
            )
 
        else:
 
            print("\n⚠ Allure report generation failed")
            print(result.stderr)
 
    except FileNotFoundError:
 
        print("\n⚠ Allure executable not found in PATH")
 
 
def pytest_addoption(parser):
 
    parser.addini(
        "testdata_file",
        "Path to Excel test data file",
        default="src/resources/testdata/TestData.xlsx"
    )
 
    parser.addini(
        "testdata_sheet",
        "Excel Sheet Name",
        default="Login"
    )
 
@pytest.fixture(scope="session")
def testdata(request):
 
    file_path = Path(
        request.config.getini("testdata_file")
    )
 
    sheet_name = request.config.getini(
        "testdata_sheet"
    )
 
    if not file_path.is_absolute():
 
        file_path = (
            Path(request.config.rootdir)
            / file_path
        )
 
    return get_test_data(
        file_path,
        sheet_name
    )