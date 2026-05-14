import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path

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