import re
import time
from playwright.sync_api import Page, expect
from src.test.pages.mc_login_page import loginpage
from src.test.pages.mc_landing_page import landingpage
from src.test.pages.mc_dashboard_page import DashboardPage
 
def test_open_login(page: Page, testdata, logger):
    """Run the login flow for each row in the Excel test data."""
    logger.info("Starting test_open_login")
 
    for idx, row in enumerate(testdata, start=1):
        username = row.get('username') or row.get('Username') or row.get('user')
        password = row.get('password') or row.get('Password') or row.get('pass')
        if not username or not password:
            raise ValueError(f"Testdata row {idx} is missing username or password: {row}")
 
        logger.info(f"Processing row {idx} with username: {username}")
 
        login = loginpage(page)
        landing = landingpage(page)
        dashboard = DashboardPage(page)
 
        page.goto("https://app-qa.myclario.ai/")
        landing.click_get_started()
        login.enter_username_and_password(username, password)
        login.click_signin()
        dashboard.handle_timezone_popup()
        assert dashboard.verify_dashboard_page(), f"Dashboard verification failed for row {idx} ({username})"
 
    logger.info("test_open_login completed successfully")
