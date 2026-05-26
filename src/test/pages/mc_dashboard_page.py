from playwright.sync_api import Page

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.dashboard_text = page.get_by_role("heading", name="Dashboard")
        self.dashboard_label = page.get_by_text("Dashboard", exact=True)
        self.timezone_popup = page.locator("[role='dialog']")
        self.keep_current_button = page.locator("//button[contains(., 'Keep Current')]")
        self.update_timezone_button = page.locator("//button[contains(., 'Update Timezone')]")
        self.close_button = page.locator("//button[span[@class='sr-only' and text()='Close']]")  # Cross/Close button

    def handle_timezone_popup(self, action="close"):
        """
        Handle the timezone mismatch modal dialog.
        :param action: "keep" → Keep Current button
                      "update" → Update Timezone button
                      "close"  → Cross (X) button
        """
        # Wait for the popup to be visible (if it appears)
        try:
            self.timezone_popup.wait_for(state="visible", timeout=5000)
        except Exception:
            # Popup didn't appear – nothing to handle
            return

        if action == "keep":
            self.keep_current_button.click()
        elif action == "update":
            self.update_timezone_button.click()
        elif action == "close":
            self.close_button.click()
        else:
            raise ValueError(f"Invalid action: {action}. Use 'keep', 'update', or 'close'.")

        # Wait for popup to disappear after clicking
        self.timezone_popup.wait_for(state="hidden", timeout=5000)

    def verify_dashboard_page(self, expected_text: str = "Dashboard") -> bool:
        """Verify dashboard page after handling popup and compare actual text."""
        try:
            self.page.wait_for_load_state("networkidle")
            dashboard_locator = self.dashboard_text.or_(self.dashboard_label).first
            dashboard_locator.wait_for(state="visible", timeout=15000)
            actual_text = dashboard_locator.inner_text().strip()
            if actual_text != expected_text:
                print(f"Dashboard text mismatch: expected '{expected_text}', got '{actual_text}'")
                return False
            print(f"Dashboard text verified: expected '{expected_text}', got '{actual_text}'")
            return True
        except Exception as e:
            print(f"Dashboard verification failed: {e}")
            return False
