# step_definitions/signup_steps.py
from src.resources.utils.excel_utils import get_test_data_by_id
from pytest_bdd import scenarios, given, when, then
from conftest import page
from src.test.pages.mc_signup_page import SignupPage
from src.test.pages.mc_verify_email_page import VerifyEmailPage
from src.test.pages.mc_landing_page import landingpage

# ===== SHARED/COMMON STEPS =====

@when("User launces the MyClario application")
def launch_application(page):
    landing_page = landingpage(page)
    landing_page.launch_application()
    landing_page.verify_landing_page()


@when("User clicks on Create Account button")
def click_create_account(page):
    landing_page = landingpage(page)
    landing_page.click_create_account()


@given("User is on the MyClario registration page")
def verify_registration_page(page):
    signup_page = SignupPage(page)
    assert signup_page.first_name.is_visible()

# ===== SCENARIO 1: Registering a new user with complete and valid details =====

# @when("User enters the valid registration details")
# def enter_valid_registration_details(page):
#     signup_page = SignupPage(page)
#     signup_page.enter_first_name("Test")
#     signup_page.enter_last_name("data2")
#     signup_page.enter_email("testdata2@gmail.com")
#     signup_page.click_country_dropdown()
#     signup_page.search_country("India")
#     signup_page.select_country_from_list("India")
#     signup_page.enter_phone_number("9876543200")
#     signup_page.enter_password("Test@123")
#     signup_page.enter_confirm_password("Test@123")
@when("User enters the valid registration details")
def enter_valid_registration_details(page, testdata):

    data = get_test_data_by_id(testdata, "TC_SIP_001")

    signup_page = SignupPage(page)

    signup_page.enter_first_name(data["FirstName"])
    signup_page.enter_last_name(data["LastName"])
    signup_page.enter_email(data["Email"])

    signup_page.click_country_dropdown()
    signup_page.search_country(data["Country"])
    signup_page.select_country_from_list(data["Country"])

    signup_page.enter_phone_number(str(data["Phone"]))

    signup_page.enter_password(data["Password"])
    signup_page.enter_confirm_password(data["ConfirmPassword"])

@then("Create Account button should be enabled")
def verify_create_account_enabled(page):
    signup_page = SignupPage(page)
    assert signup_page.is_create_account_enabled()


@when("User clicks on Create account to submit the registration form")
def click_create_account_submit(page):
    signup_page = SignupPage(page)
    signup_page.click_create_account()


@then("User should navigate to Verify Your Email page")
def verify_verify_email_page(page):
    verify_email_page = VerifyEmailPage(page)
    assert verify_email_page.verify_email_page_displayed()

# ===== SCENARIO 2: Registering a new user with incomplete details =====

# @when("User does not enter the valid registration details")
# def enter_incomplete_registration_details(page):
#     signup_page = SignupPage(page)
#     signup_page.enter_first_name("Rohitha")
#     signup_page.enter_last_name("Koya")
#     signup_page.click_country_dropdown()
#     signup_page.search_country("India")
#     signup_page.select_country_from_list("India")
#     signup_page.enter_phone_number("9876543210")
#     signup_page.enter_password("Test@123")
#     signup_page.enter_confirm_password("Test@123")
@when("User does not enter the valid registration details")
def enter_incomplete_registration_details(page, testdata):

    data = get_test_data_by_id(testdata, "TC_SIP_002")

    signup_page = SignupPage(page)

    signup_page.enter_first_name(data["FirstName"])
    signup_page.enter_last_name(data["LastName"])

    signup_page.click_country_dropdown()
    signup_page.search_country(data["Country"])
    signup_page.select_country_from_list(data["Country"])

    signup_page.enter_phone_number(str(data["Phone"]))

    signup_page.enter_password(data["Password"])
    signup_page.enter_confirm_password(data["ConfirmPassword"])

@then("We receive an error message indicating that email is required")
def verify_email_required_error(page):
    signup_page = SignupPage(page)
    expected_error = "Please fill out this field."
    actual_error = signup_page.get_email_required_error()
    assert expected_error in actual_error

# ===== SCENARIO 3: Duplicate Email Validation =====

@when("User enters duplicate email details")
# def enter_duplicate_email(page):
#     signup_page = SignupPage(page)
#     signup_page.enter_first_name("Rohitha")
#     signup_page.enter_last_name("Koya")
#     signup_page.enter_email("rohita.koya@bilvantis.io")

@when("User enters duplicate email details")
def enter_duplicate_email(page, testdata):

    data = get_test_data_by_id(testdata, "TC_SIP_003")

    signup_page = SignupPage(page)

    signup_page.enter_first_name(data["FirstName"])
    signup_page.enter_last_name(data["LastName"])
    signup_page.enter_email(data["Email"])


@when("User enters the remaining details")
def enter_remaining_details(page, testdata):
    data = get_test_data_by_id(testdata, "TC_SIP_003")

    signup_page = SignupPage(page)

    signup_page.click_country_dropdown()
    signup_page.search_country(data["Country"])
    signup_page.select_country_from_list(data["Country"])

    signup_page.enter_phone_number(str(data["Phone"]))

    signup_page.enter_password(data["Password"])
    signup_page.enter_confirm_password(data["ConfirmPassword"])


@when("User clicks on Create Account submit button")
def click_create_account_button(page):
    signup_page = SignupPage(page)
    signup_page.click_create_account()


@then("Duplicate email error message should be displayed")
def verify_duplicate_email_error(page):
    signup_page = SignupPage(page)
    expected_error = (
        "An account with this email already exists. "
        "Please sign in instead."
    )
    actual_error = signup_page.duplicate_email_error.text_content()
    assert expected_error in actual_error

# ===== SCENARIO 4: Sign In Navigation =====

@when("User clicks on Sign In link")
def click_sign_in_link(page):
    signup_page = SignupPage(page)
    signup_page.click_sign_in_link()


@then("User should navigate to Sign In page")
def verify_sign_in_navigation(page):
    assert "auth" in page.url.lower()

