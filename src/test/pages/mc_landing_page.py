from playwright.sync_api import Page


class landingpage:
    def __init__(self, page:Page):
        self.page = page
        self.get_started = page.get_by_role("button", name="Get Started")
        self.createaccount = page.get_by_role("button", name="Create Account")
        self.termsandconditions = page.get_by_role("text", name="Terms and Conditions")
        self.privacypolicy = page.get_by_role("text", name="Privacy Policy")
        self.landing_page_verification = page.get_by_role("heading", name="myClario – Your smart")

    def launch_application(self): 
        self.page.goto("https://app-qa.myclario.ai/", wait_until="networkidle" )

        
    def click_get_started(self):
        self.get_started.click()
        
    def click_create_account(self):
        self.createaccount.click() 
    
    def click_terms_and_conditions(self):
        self.termsandconditions.click()
        
    def click_privacy_policy(self):
        self.privacypolicy.click()  
    
    def verify_landing_page(self) -> bool:
        # Wait a bit to ensure heading is present (Playwright auto-waits, but explicit is fine)
        return self.landing_page_verification.is_visible()           