import re

from playwright.sync_api import expect
from pytest_bdd import given, then, when

from src.test.pages.mc_dashboard_page import DashboardPage
from src.test.pages.mc_landing_page import landingpage
from src.test.pages.mc_login_page import loginpage


@given("I open the MyClario application")
def open_application(page):
    page.goto("https://app-qa.myclario.ai/")


@when("I click the Get Started button")
def click_get_started(page):
    landing = landingpage(page)
    landing.click_get_started()


@when("I login with valid credentials")
def login_with_valid_credentials(page, testdata):
    row = testdata[0]
    login = loginpage(page)
    login.enter_username_and_password(row["username"], row["password"])
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
