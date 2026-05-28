from playwright.sync_api import Page


class loginpage:
    def __init__(self, page:Page):
        self.page = page
        self.username = page.get_by_role("textbox", name="Email")
        self.password = page.get_by_role("textbox", name="Password")
        self.signin = page.get_by_role("button", name="Sign In")
        
    def enter_username_and_password(self, username, password:str):
        self.username.fill(username)
        self.password.fill(password)
        
    def click_signin(self):
        self.signin.click()
        