import re
from playwright.sync_api import Page, expect

class loginpage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_role("textbox", name=re.compile("email", re.I))
        self.password = page.get_by_role("textbox", name=re.compile("password", re.I))
        self.signin = page.get_by_role("button", name=re.compile("sign in", re.I))
        self.sigintext=page.locator("xpath=//h3[text()='Sign In']")
        self.forgot_password = page.locator("//button[normalize-space(text())='Forgot Password?']")
        self.sign_up = page.locator("//button[@type='button' and contains(text(), 'Sign up')]")
        self.invalidCredErrorMessage = page.locator("(//div[@class='grid gap-1'])[2]")
        
        
        
        
    def enter_username_and_password(self, username, password :str):
        self.username.fill(username)
        self.password.fill(password)
        
    def click_signin(self):
        self.signin.click()

    def enter_email(self, email: str):
        self.username.fill(email)

    def click_forgot_password(self):
        self.forgot_password.click()

    def click_sign_up(self):
        self.sign_up.first.click()
        
    def is_error_message_displayed(self, timeout=5000):
      try:
        self.invalidCredErrorMessage.wait_for(state="visible", timeout=timeout)
        return self.invalidCredErrorMessage.is_visible()
      except:
        return False
        # return self.invalidCredErrorMessage.text_content()

    def verify_login_page(self):
        return self.sigintext.is_visible()
    
    def validate_page_message(self, pattern, timeout=20000, error_message=""):
        """
        Generic method to validate any message/text on the page.
        
        Args:
            pattern: String, regex pattern, or compiled regex to search for
            timeout: Timeout in milliseconds (default 20000)
            error_message: Custom error message to display if validation fails
        
        Returns:
            True if the pattern is found on the page body
            
        Raises:
            AssertionError with descriptive message if pattern not found
        """
        try:
            # Convert string to regex if needed
            if isinstance(pattern, str):
                pattern = re.compile(pattern, re.I)
            
            # Check if pattern exists on page body
            expect(self.page.locator("body")).to_contain_text(pattern, timeout=timeout)
            return True
            
        except AssertionError as e:
            # Provide clear error message
            if error_message:
                raise AssertionError(f"{error_message}\nActual page text did not match pattern: {pattern.pattern if hasattr(pattern, 'pattern') else pattern}") from e
            else:
                raise AssertionError(f"Expected to find pattern '{pattern.pattern if hasattr(pattern, 'pattern') else pattern}' on the page, but it was not found") from e
  
        