import re
import time
from playwright.sync_api import Page, expect
from conftest import page
from pages.mc_login_page import loginpage
from pages.mc_landing_page import landingpage
from pages.mc_dashboard_page import DashboardPage

def test_open_login(page: Page):
    login = loginpage(page)
    landing = landingpage(page)
    dashboard = DashboardPage(page)
    page.goto("https://app-qa.myclario.ai/")
    landing.click_get_started()
    login.enter_username_and_password("manoj.behera@bilvantis.io", "Steephen@1291")
    login.click_signin()
    dashboard.handle_timezone_popup()
    dashboard.verify_dashboard_page()
    #assert dashboard.verify_dashboard_page(), "Dashboard verification failed"
def test_open_login(page: Page, testdata):
    """Run the login flow for each row in the Excel test data.

    Expected columns: `username`, `password` (case-insensitive).
    """
    for idx, row in enumerate(testdata, start=1):
        username = row.get('username') or row.get('Username') or row.get('user')
        password = row.get('password') or row.get('Password') or row.get('pass')
        if not username or not password:
            raise ValueError(f"Testdata row {idx} is missing username or password: {row}")

        login = loginpage(page)
        landing = landingpage(page)
        dashboard = DashboardPage(page)

        page.goto("https://app-qa.myclario.ai/")
        landing.click_get_started()
        login.enter_username_and_password(username, password)
        login.click_signin()
        dashboard.handle_timezone_popup()
        assert dashboard.verify_dashboard_page(), f"Dashboard verification failed for row {idx} ({username})"

    
