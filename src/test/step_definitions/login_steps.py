import re

from playwright.sync_api import expect
from pytest_bdd import given, then, when, parsers

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


def _login_with_credentials(page, username, password):
    """Reusable login helper for valid, invalid, and empty credentials."""
    login = loginpage(page)
    login.enter_username_and_password(username, password)
    login.click_signin()


@when(parsers.parse("I login with {credential_type} credentials"))
def login_with_credentials(page, testdata, credential_type):
    credential_type = credential_type.lower().strip()

    if credential_type == "valid":
        username = testdata[0]["username"]
        password = testdata[0]["password"]
    elif credential_type in {"invalid", "wrong"}:
        username = "wrong.user@example.com"
        password = "WrongPassword@123"
    elif credential_type in {"empty", "blank", "none"}:
        username = ""
        password = ""
    else:
        raise ValueError(f"Unsupported credential type: {credential_type}")

    _login_with_credentials(page, username, password)

    # Keep the original expectation for successful login path only.
    if credential_type == "valid":
        expect(page).not_to_have_url(re.compile(r".*/auth.*"), timeout=10000)


@when("I handle the timezone popup")
def handle_timezone_popup(page):
    dashboard = DashboardPage(page)
    dashboard.handle_timezone_popup()


@then("I should see the dashboard page")
def verify_dashboard(page):
    dashboard = DashboardPage(page)
    assert dashboard.verify_dashboard_page()


@when("User has successfully landed on the login page")
def verify_login_page_loaded(page):
    login = loginpage(page)
    login.verify_login_page()


@when("I enter a registered email address")
def enter_registered_email(page, testdata):
    email = testdata[0].get("username") or testdata[0].get("email") or ""
    login = loginpage(page)
    login.enter_email(email)


@when("I enter an unregistered email address")
def enter_unregistered_email(page):
    login = loginpage(page)
    login.enter_email("notregistered@example.com")


@when("I click the Forgot Password link")
def click_forgot_password(page):
    login = loginpage(page)
    login.click_forgot_password()


@when("I click the Sign Up link")
def click_sign_up(page):
    login = loginpage(page)
    login.click_sign_up()


@then("I should see a confirmation message that the password reset link has been sent to the email address")
def assert_reset_link_message(page):
    login = loginpage(page)
    login.validate_page_message("confirmation|link.*sent|email.*received", error_message="Expected confirmation message for password reset link")
@then("I should see an error message that the email address is not registered")
def assert_unregistered_email_error(page):
    login = loginpage(page)
    login.validate_page_message("no account found|invalid email", error_message="Expected error message for unregistered email")


@then("I should see an error message")
def assert_generic_error(page):
    login = loginpage(page)
    login.validate_page_message("error|invalid|incorrect|required|cannot be empty", error_message="Expected error message on login page")
@then("I should be redirected to the registration page")
def assert_registration_page(page):
    login = loginpage(page)
    login.validate_page_message("create account|Create New Account|sign up|register", error_message="Expected to be on the registration page after clicking Sign Up link")

@then("verify that user still remains on the login page")
def assert_still_on_login_page(page):
    login = loginpage(page)
    assert login.verify_login_page() 