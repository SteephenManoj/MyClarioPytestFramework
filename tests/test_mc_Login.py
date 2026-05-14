import re
import time
from playwright.sync_api import Page, expect
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

    
