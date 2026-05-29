import re
import os
from pathlib import Path

from playwright.sync_api import expect
from pytest_bdd import given, then, when

from src.test.pages.mc_dashboard_page import DashboardPage
from src.test.pages.mc_landing_page import landingpage
from src.test.pages.mc_login_page import loginpage


def _get_base_url():
    env_name = os.getenv("MYCLARIO_ENV", "").upper()
    env_url = os.getenv(f"MYCLARIO_{env_name}_BASE_URL") if env_name else None
    return env_url or os.getenv("MYCLARIO_BASE_URL", "https://app-qa.myclario.ai/")


@given("I open the MyClario application")
def open_application(page):
    page.goto(_get_base_url())


@when("I click the Get Started button")
def click_get_started(page):
    landing = landingpage(page)
    landing.click_get_started()


@when("I login with valid credentials")
def login_with_valid_credentials(page, testdata):
    base_url = _get_base_url().rstrip("/")

    try:
        page.get_by_role("button", name="Get Started").wait_for(state="visible", timeout=5000)
    except Exception:
        page.goto(f"{base_url}/dashboard")
        try:
            page.get_by_text("Dashboard", exact=True).wait_for(state="visible", timeout=15000)
            return
        except Exception:
            page.goto(_get_base_url())

    row = testdata[0]
    username = os.getenv("MYCLARIO_USERNAME") or row["username"]
    password = os.getenv("MYCLARIO_PASSWORD") or row["password"]

    login = loginpage(page)
    login.enter_username_and_password(username, password)
    login.click_signin()
    expect(page).not_to_have_url(re.compile(r".*/auth.*"), timeout=60000)

    auth_state_path = Path("reports/auth/storage_state.json")
    auth_state_path.parent.mkdir(parents=True, exist_ok=True)
    page.context.storage_state(path=str(auth_state_path))


@when("I handle the timezone popup")
def handle_timezone_popup(page):
    dashboard = DashboardPage(page)
    dashboard.handle_timezone_popup()


@then("I should see the dashboard page")
def verify_dashboard(page):
    dashboard = DashboardPage(page)
    assert dashboard.verify_dashboard_page()
