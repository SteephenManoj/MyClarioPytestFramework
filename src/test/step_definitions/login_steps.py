import re
import os

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
    row = testdata[0]
    username = os.getenv("MYCLARIO_USERNAME") or row["username"]
    password = os.getenv("MYCLARIO_PASSWORD") or row["password"]

    login = loginpage(page)
    login.enter_username_and_password(username, password)
    login.click_signin()
    expect(page).not_to_have_url(re.compile(r".*/auth.*"), timeout=10000)


@when("I handle the timezone popup")
def handle_timezone_popup(page):
    dashboard = DashboardPage(page)
    dashboard.handle_timezone_popup()


@then("I should see the dashboard page")
def verify_dashboard(page):
    dashboard = DashboardPage(page)
    assert dashboard.verify_dashboard_page()
