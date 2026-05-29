from playwright.sync_api import Page

class VerifyEmailPage:
    def __init__(self, page):
        self.page = page
        self.verify_email_heading = page.get_by_role("heading", name="Verify Your Email")
        self.resend_verification_button = page.get_by_role("button", name="Resend Verification Email")
        self.go_to_signin_button = page.get_by_role("button", name="Go to Sign In")

    def verify_email_page_displayed(self):
        return self.verify_email_heading.is_visible()

    def click_resend_verification_email(self):
        self.page.click(self.resend_verification_button)

    def click_go_to_signin(self):
        self.page.click(self.go_to_signin_button)