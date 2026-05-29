from playwright.sync_api import Page


class SignupPage:
    def __init__(self, page):
        self.page = page
        self.first_name = page.get_by_role("textbox", name="First Name *")
        self.last_name = page.get_by_role("textbox", name="Last Name")
        self.email = page.get_by_role("textbox", name="Email *")
        self.country_dropdown = page.locator("xpath=//div[@class='selected-flag']")
        self.phone = page.get_by_role("textbox", name="1 (702) 123-")
        self.password = page.get_by_role("textbox", name="Password *", exact=True)
        self.confirm_password =page.get_by_role("textbox", name="Confirm Password *")
        self.country_search = page.locator("xpath=//input[@class='search-box']")
        self.create_account_button =page.get_by_role("button", name="Create Account")
        self.sign_in_link =page.get_by_role("button", name="Already have an account? Sign")

        self.duplicate_email_error = page.get_by_text(
            "An account with this email already exists"
        ).first


    def enter_first_name(self, firstname):
        self.first_name.fill(firstname)

    def enter_last_name(self, lastname):
        self.last_name.fill(lastname)

    def enter_email(self, email):
        self.email.fill(email)

    def click_country_dropdown(self):
        self.country_dropdown.click()

    def search_country(self, country): 
        self.country_search.fill(country)
    
    def select_country_from_list(self, country):
        country_locator = self.page.locator( f"//span[@class='country-name' and text()='{country}']" ) 
        country_locator.scroll_into_view_if_needed()
        country_locator.wait_for(state="visible") 
        country_locator.click()

    def enter_phone_number(self, phone):
        self.phone.click() 
        self.phone.press("Control+A") 
        self.phone.press("ArrowRight") 
        self.phone.type(phone)

    def enter_password(self, password):
        self.password.fill(password)

    def enter_confirm_password(self, confirm_password):
        self.confirm_password.fill(confirm_password)

    def click_create_account(self):
        self.create_account_button.click()

    def is_create_account_disabled(self):
        return self.create_account_button.is_disabled()
    
    def is_create_account_enabled(self):
        return self.create_account_button.is_enabled()
    
    
    def click_sign_in_link(self):
        self.sign_in_link.click()

    def get_duplicate_email_error(self):
        return self.duplicate_email_error.text_content()
    
    def get_email_required_error(self):
        return self.email.evaluate("el => el.validationMessage")