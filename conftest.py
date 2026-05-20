import base64
from datetime import datetime

import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
from slugify import slugify
import allure

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
        yield browser
        browser.close()

@pytest.fixture
def page(browser, request):
    # Create a new context with tracing enabled and inherit the desktop window size
    context = browser.new_context(no_viewport=True)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    # Create a page from the context
    page = context.new_page()
    
    yield page
    
    # After test finishes, stop tracing and save the trace
    trace_path = Path(f"traces/{request.node.name}.zip")
    trace_path.parent.mkdir(exist_ok=True)
    context.tracing.stop(path=str(trace_path))
    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    setattr(item, "rep_" + report.when, report)

    # Execute only after test execution phase
    if report.when == "call":

        if "page" in item.funcargs:

            page = item.funcargs["page"]

            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            # PASS / FAIL naming
            status = "PASSED" if report.passed else "FAILED"

            # screenshot_path = screenshot_dir / f"{slugify(item.nodeid)}_{status}.png"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshot_dir /(f"{slugify(item.nodeid)}_{status}_{timestamp}.png")

            # Capture screenshot
            page.screenshot(path=str(screenshot_path))

            # Read screenshot bytes
            screenshot_bytes = screenshot_path.read_bytes()

            # Attach to Allure
            allure.attach(
                screenshot_bytes,
                name=f"{status} Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # Attach to pytest-html
            pytest_html = item.config.pluginmanager.getplugin("html")

            if pytest_html:

                extras = getattr(report, "extras", [])

                extras.append(
                    pytest_html.extras.png(
                        base64.b64encode(screenshot_bytes).decode("utf-8")
                    )
                )

                report.extras = extras