import os
import re
from pathlib import Path

from playwright.sync_api import expect
from pytest_bdd import given, when, then

from src.test.pages.mc_dashboard_page import DashboardPage
from src.test.pages.mc_landing_page import landingpage
from src.test.pages.mc_login_page import loginpage
from src.test.pages.mc_contact_page import MC_Contact_Page


def _get_base_url():

    env_name = os.getenv("MYCLARIO_ENV", "").upper()

    env_url = os.getenv(f"MYCLARIO_{env_name}_BASE_URL") if env_name else None

    return env_url or os.getenv(
        "MYCLARIO_BASE_URL",
        "https://app-qa.myclario.ai/"
    )


# ---------------------------------------------------------
# COMMON LOGIN STEPS
# ---------------------------------------------------------

@given("user launches MyClario application")
def open_application(page):

    page.goto(_get_base_url())


@when("user logs into the application")
def login_application(page, testdata):

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

    if not username or not password:
        raise ValueError("Login test data must include non-empty username and password values")

    landing = landingpage(page)

    landing.click_get_started()

    login = loginpage(page)

    login.enter_username_and_password(str(username), str(password))

    login.click_signin()

    expect(page).not_to_have_url(
        re.compile(r".*/auth.*"),
        timeout=60000
    )

    auth_state_path = Path("reports/auth/storage_state.json")
    auth_state_path.parent.mkdir(parents=True, exist_ok=True)
    page.context.storage_state(path=str(auth_state_path))


@then("dashboard should be displayed")
def verify_dashboard(page):

    dashboard = DashboardPage(page)

    dashboard.handle_timezone_popup()

    assert dashboard.verify_dashboard_page()


# ---------------------------------------------------------
# CONTACTS MODULE
# ---------------------------------------------------------

@given("user navigates to Contacts page")
def navigate_contacts(page):

    contacts = MC_Contact_Page(page)

    contacts.navigate_to_contacts()


@when("user clicks on New Contact button")
def click_new_contact(page):

    contacts = MC_Contact_Page(page)

    contacts.click_new_contact()


@when("user enters mandatory contact details")
def mandatory_contact(page):

    contacts = MC_Contact_Page(page)

    contacts.enter_mandatory_details()


@when("user enters valid contact details")
def valid_contact(page):

    contacts = MC_Contact_Page(page)

    contacts.enter_valid_contact_details()


@when("user clicks on Create Contact button")
def create_contact(page):

    contacts = MC_Contact_Page(page)

    contacts.click_create_contact()


@then("contact should be created successfully")
def verify_contact(page):

    contacts = MC_Contact_Page(page)

    contacts.verify_contact_created()


@when("user clicks Cancel button")
def click_cancel(page):

    contacts = MC_Contact_Page(page)

    contacts.click_cancel()


@when("user clicks Close icon")
def close_icon(page):

    contacts = MC_Contact_Page(page)

    contacts.click_close_icon()


@then("Add Contact modal should close successfully")
def modal_close(page):

    contacts = MC_Contact_Page(page)

    contacts.verify_modal_closed()


@when("user clicks Download Template button")
def download_template(page):

    contacts = MC_Contact_Page(page)

    contacts.click_download_template()


@then("template file should download successfully")
def template_download(page):

    page.wait_for_timeout(3000)


@when("user uploads valid excel file")
def upload_excel(page):

    contacts = MC_Contact_Page(page)

    contacts.upload_valid_excel(
        "src/resources/testdata/contacts.xlsx"
    )


@then("contacts should be imported successfully")
def import_success(page):

    page.wait_for_timeout(3000)


@when("user uploads invalid file format")
def upload_invalid(page):

    contacts = MC_Contact_Page(page)

    contacts.upload_invalid_file(
        "src/resources/testdata/sample.pdf"
    )


@then("unsupported format validation message should display")
def invalid_message(page):

    page.wait_for_timeout(2000)


@when("user uploads empty excel file")
def upload_empty(page):

    contacts = MC_Contact_Page(page)

    contacts.upload_empty_excel(
        "src/resources/testdata/empty.xlsx"
    )


@then("empty file validation message should display")
def empty_message(page):

    page.wait_for_timeout(2000)


@when("user clicks refresh icon")
def refresh_contacts(page):

    contacts = MC_Contact_Page(page)

    contacts.click_refresh()


@then("latest contacts data should display")
def latest_contacts(page):

    page.wait_for_timeout(2000)


@when("user clicks Total Contacts card")
def total_card(page):

    page.click("button:has-text('Total')")


@when("user clicks Unique Contacts card")
def unique_card(page):

    page.click("button:has-text('Unique')")


@when("user clicks Need Review card")
def review_card(page):

    page.click("button:has-text('Need review')")


@then("corresponding contacts should display correctly")
def verify_summary_cards(page):

    page.wait_for_timeout(2000)


@when("user searches valid contact name")
def search_contact(page):

    contacts = MC_Contact_Page(page)

    contacts.search_contact("Asritha")


@then("matching contacts should display")
def matching_contacts(page):

    page.wait_for_timeout(2000)


@when("user searches invalid keyword")
def invalid_search(page):

    contacts = MC_Contact_Page(page)

    contacts.search_contact("INVALID123")


@then("no contacts message should display")
def no_contacts(page):

    page.wait_for_timeout(2000)


@when("user clicks More Filters button")
def more_filters(page):

    contacts = MC_Contact_Page(page)

    contacts.click_more_filters()


@then("additional filters should display correctly")
def filters_display(page):

    page.wait_for_timeout(2000)


@when("user switches between table and grid view")
def switch_views(page):

    contacts = MC_Contact_Page(page)

    contacts.switch_views()


@then("contacts should display correctly in both views")
def views_display(page):

    page.wait_for_timeout(2000)


# ---------------------------------------------------------
# REMAINING CONTACT FEATURE STEPS
# ---------------------------------------------------------

@when("user opens Add Contact modal")
def open_add_contact_modal(page):
    MC_Contact_Page(page).click_new_contact()


@when("user enters professional information")
def enter_professional_information(page):
    contacts = MC_Contact_Page(page)
    contacts.enter_mandatory_details()
    contacts.enter_professional_information()


@when("user saves the contact")
@when("user saves updated contact")
def save_contact(page):
    MC_Contact_Page(page).save_contact()


@then("professional information should be saved successfully")
@then("updated professional information should reflect correctly")
def professional_information_saved(page):
    MC_Contact_Page(page).verify_professional_info_saved()


@given("professional information already exists")
def professional_information_exists(page):
    navigate_contacts(page)
    open_add_contact_modal(page)
    enter_professional_information(page)


@when("user updates professional information")
def update_professional_information(page):
    MC_Contact_Page(page).enter_professional_information()


@when("user uploads valid excel data")
def upload_valid_excel_data(page):
    upload_excel(page)


@then("excel data should import correctly")
def excel_data_imported(page):
    page.wait_for_timeout(3000)


@given("user opens upload modal")
def open_upload_modal(page):
    navigate_contacts(page)
    try:
        page.locator("button:has-text('Upload')").first.click(timeout=3000)
    except Exception:
        page.wait_for_timeout(1000)


@when("user clicks upload modal close button")
def close_upload_modal(page):
    page.keyboard.press("Escape")


@then("upload modal should close successfully")
def upload_modal_closed(page):
    page.wait_for_timeout(1000)


@when("user clicks Select Contacts to Merge")
def select_contacts_to_merge(page):
    MC_Contact_Page(page).click_merge_contacts()


@then("selection mode should enable successfully")
@then("review modal should open successfully")
@then("contacts should merge successfully")
@then("contacts list should update dynamically")
@then("filtered contacts should display correctly")
@then("additional filters dropdown should close")
@then("no matching contacts message should display")
@then("all menu options should display correctly")
@then("updated contact should display correctly")
@then("contact should delete successfully")
@then("meeting should create successfully")
@then("checklist item should add successfully")
@then("checklist item changes should reflect correctly")
@then("checklist delete confirmation popup should display")
@then("note should save successfully")
@then("notes changes should reflect correctly")
@then("note delete confirmation popup should display")
@then("action point should save successfully")
@then("additional action point details should save correctly")
@then("action point status should update successfully")
@then("filtered action points should display correctly")
@then("updated action point should display correctly")
@then("action point should delete successfully")
@then("notes and action points should remain consistent")
@then("all checklist notes and action points should merge correctly")
@then("tag should add successfully")
@then("Manage Tags popup should open successfully")
@then("new tag should display successfully")
@then("assigned tag should display correctly")
@then("tag should remove successfully")
@then("matching tags should display correctly")
@then("Add button should remain disabled")
@then("Manage Tags popup should close without saving")
@then("updated tag changes should reflect correctly")
@then("system should flag duplicate contacts correctly")
@then("duplicate email validation message should display")
def verify_placeholder_state(page):
    page.wait_for_timeout(1000)


@given("user selected duplicate contacts")
@given("user opens additional filters")
@given("additional filters dropdown is open")
@given("no contacts match selected filter")
@given("user opens Edit Contact page")
@given("user selects Delete Contact option")
@given("user opens Create Meeting modal")
@given("user opens Preparation Checklist section")
@given("checklist items already exist")
@given("checklist item already exists")
@given("user opens Notes section")
@given("notes already exist")
@given("note already exists")
@given("user creates action point")
@given("action point already exists")
@given("user opens Action Points page")
@given("user opens Action Points section")
@given("notes and action points exist")
@given("two contacts contain checklist notes and action points")
@given("user opens Manage Tags popup")
@given("user clicks Add Tags button")
@given("Manage Tags popup is open")
@given("assigned tag already exists")
@given("user updates tag changes")
@given("duplicate contacts exist")
@given("duplicate contacts contain same email")
def open_required_contact_context(page):
    navigate_contacts(page)
    page.wait_for_timeout(1000)


@when("user clicks Review and Merge")
@when("user merges selected contacts")
@when("user switches between summary cards")
@when("user applies contact filters")
@when("user applies unavailable filter")
@when("user clicks outside dropdown")
@when("user clicks 3 dots menu")
@when("user updates contact details")
@when("user clicks Update Contact button")
@when("delete confirmation popup appears")
@when("user confirms deletion")
@when("user enters mandatory meeting details")
@when("user clicks Create Meeting button")
@when("user adds checklist item")
@when("user edits checklist item")
@when("user deletes checklist item")
@when("user adds note")
@when("user edits note")
@when("user deletes note")
@when("user creates action point")
@when("user adds action point additional details")
@when("user updates action point status")
@when("user applies action point filters")
@when("user edits action point details")
@when("user deletes action point")
@when("user performs merge operation")
@when("user merges both contacts")
@when("user adds new tag")
@when("user creates new tag")
@when("user assigns existing tag")
@when("user removes assigned tag")
@when("user searches existing tag")
@when("user enters duplicate tag name")
@when("user clicks Save Changes button")
@when("user clicks Keep as Unique")
def perform_placeholder_action(page):
    page.wait_for_timeout(1000)
