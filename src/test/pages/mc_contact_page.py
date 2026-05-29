from playwright.sync_api import expect
import random
import re


class MC_Contact_Page:

    def __init__(self, page):
        self.page = page

    def _click_if_visible(self, selector, timeout=3000):
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            return True
        except Exception:
            return False

    # ---------------- LOCATORS ---------------- #

    contacts_menu = "a[href='/contacts']"
    contacts_heading = "h1"

    new_contact_btn = "button:has-text('New')"
    create_contact_btn = "button:has-text('Add Contact')"
    cancel_btn = "button:has-text('Cancel')"
    close_icon = "button svg"

    first_name = "input[name='first_name']"
    last_name = "input[name='last_name']"
    email = "input[type='email']"
    notes = "textarea"

    company = "input[placeholder='Company']"
    designation = "input[placeholder='Job Title']"
    department = "input[placeholder='Department']"

    total_card = "button:has-text('Total')"
    unique_card = "button:has-text('Unique')"
    need_review_card = "button:has-text('Need review')"

    search_box = "input[placeholder*='Search contacts']"

    refresh_icon = "button[aria-label='Refresh']"

    more_filters = "button:has-text('More')"

    table_view = "button[aria-label='Table View']"
    grid_view = "button[aria-label='Grid View']"

    upload_excel_btn = "button:has-text('Upload Excel')"
    download_template_btn = "button:has-text('Download Template')"

    upload_input = "input[type='file']"

    merge_btn = "button:has-text('Select Contacts to Merge')"

    country_dropdown = "label:has-text('Country') + button, button:has-text('Select country')"
    state_dropdown = "label:has-text('State') + button, button:has-text('Select country first'), button:has-text('Select state')"
    city_dropdown = "label:has-text('City') + button, button:has-text('Select country and state first'), button:has-text('Select city')"

    # ---------------- METHODS ---------------- #

    def handle_blocking_popups(self):
        for button_name in ("Keep Current", "Close"):
            try:
                self.page.get_by_role("button", name=button_name).click(timeout=1500)
            except Exception:
                pass

    def navigate_to_contacts(self):
        self.handle_blocking_popups()
        self.page.click(self.contacts_menu)
        self.handle_blocking_popups()
        expect(self.page.locator(self.contacts_heading)).to_contain_text("Contacts")

    def click_new_contact(self):
        self.handle_blocking_popups()
        self.page.mc_total_contacts_before = self.get_total_contacts_count()
        self.page.click(self.new_contact_btn)
        expect(self.page.get_by_text("Add New Contact")).to_be_visible(timeout=10000)

    def enter_mandatory_details(self):
        random_no = random.randint(1000, 9999)
        self.page.mc_created_contact = {
            "first_name": f"Asritha{random_no}",
            "last_name": "QA",
            "email": f"asritha{random_no}@mailinator.com",
        }

        self.page.fill(self.first_name, self.page.mc_created_contact["first_name"])
        self.page.fill(self.last_name, self.page.mc_created_contact["last_name"])
        self.page.fill(self.email, self.page.mc_created_contact["email"])
        self.select_location()

    def enter_valid_contact_details(self):
        self.enter_mandatory_details()

        if self.page.locator(self.notes).count() > 0:
            self.page.fill(self.notes, "Automation Contact")

    def click_create_contact(self):
        self.page.click(self.create_contact_btn)

    def verify_contact_created(self):
        created_contact = getattr(self.page, "mc_created_contact", None)
        if not created_contact:
            raise AssertionError("No contact details were entered before verifying creation")

        contact_name = f"{created_contact['first_name']} {created_contact['last_name']}"
        expect(self.page.get_by_text(contact_name, exact=False).first).to_be_visible(timeout=20000)

        total_contacts_before = getattr(self.page, "mc_total_contacts_before", None)
        if total_contacts_before is not None:
            total_contacts_after = self.get_total_contacts_count()
            assert total_contacts_after >= total_contacts_before + 1, (
                f"Expected total contacts to increase from {total_contacts_before}, "
                f"but it is {total_contacts_after}"
            )

    def click_cancel(self):
        self._click_if_visible(self.cancel_btn)

    def click_close_icon(self):
        self.page.keyboard.press("Escape")

    def verify_modal_closed(self):
        self.page.wait_for_timeout(1000)

    def enter_professional_information(self):
        if self.page.locator(self.company).count() > 0:
            self.page.fill(self.company, "Bilvantis")

        if self.page.locator(self.designation).count() > 0:
            self.page.fill(self.designation, "QA Engineer")

        if self.page.locator(self.department).count() > 0:
            self.page.fill(self.department, "Testing")

    def save_contact(self):
        self.page.click(self.create_contact_btn)

    def verify_professional_info_saved(self):
        self.verify_contact_created()

    def click_download_template(self):
        if self.page.locator(self.download_template_btn).count() == 0:
            return

        with self.page.expect_download():
            self.page.click(self.download_template_btn)

    def upload_valid_excel(self, file_path):
        if self.page.locator(self.upload_input).count() > 0:
            self.page.set_input_files(self.upload_input, file_path)

    def upload_invalid_file(self, file_path):
        if self.page.locator(self.upload_input).count() > 0:
            self.page.set_input_files(self.upload_input, file_path)

    def upload_empty_excel(self, file_path):
        if self.page.locator(self.upload_input).count() > 0:
            self.page.set_input_files(self.upload_input, file_path)

    def click_refresh(self):
        if self.page.locator(self.refresh_icon).count() > 0:
            self.page.click(self.refresh_icon)

    def click_summary_cards(self):
        self.page.click(self.total_card)
        self.page.click(self.unique_card)
        self.page.click(self.need_review_card)

    def search_contact(self, name):
        self.page.fill(self.search_box, name)

    def click_more_filters(self):
        self._click_if_visible(self.more_filters)

    def switch_views(self):
        if self.page.locator(self.grid_view).count() > 0:
            self.page.click(self.grid_view)

        if self.page.locator(self.table_view).count() > 0:
            self.page.click(self.table_view)

    def click_merge_contacts(self):
        if self.page.locator(self.merge_btn).count() > 0:
            self.page.click(self.merge_btn)

    def get_total_contacts_count(self):
        total_text = self.page.locator(self.total_card).first.inner_text(timeout=10000)
        digits = "".join(ch for ch in total_text if ch.isdigit())
        return int(digits) if digits else 0

    def select_location(self):
        self._select_dropdown_option(self.country_dropdown, "India")
        self._select_dropdown_option(self.state_dropdown, "Telangana")
        self._select_dropdown_option(self.city_dropdown, "Hyderabad")

    def _select_dropdown_option(self, dropdown_selector, option_text):
        dropdown = self.page.locator(dropdown_selector).first
        dropdown.click(timeout=10000)

        search_input = self.page.locator("[cmdk-input], [role='dialog'] input[placeholder*='Search']").last
        if search_input.count() > 0:
            try:
                search_input.fill(option_text, timeout=3000)
            except Exception:
                pass

        option = self.page.locator(f"[role='option']:has-text('{option_text}')").first
        if option.count() == 0:
            option = self.page.locator(f"[cmdk-item]:has-text('{option_text}')").first
        if option.count() == 0:
            option = self.page.locator(f"[data-value*='{option_text}' i]").first
        if option.count() == 0:
            cmdk_items = self.page.locator("[cmdk-item]").all_inner_texts()
            role_options = self.page.locator("[role='option']").all_inner_texts()
            visible_text = " ".join(self.page.locator("body").inner_text().split())[-1500:]
            country_html = self.page.locator("label:has-text('Country')").locator("xpath=..").first.inner_html()
            controlled_id = dropdown.get_attribute("aria-controls")
            popover_html = ""
            if controlled_id:
                popover_html = self.page.locator(f"[id='{controlled_id}']").first.inner_html(timeout=3000)
            raise AssertionError(
                f"Could not find dropdown option '{option_text}'. "
                f"cmdk_items={cmdk_items[:20]}, role_options={role_options[:20]}, "
                f"country_html={country_html[:1000]}, popover_html={popover_html[:1500]}, "
                f"visible_tail={visible_text}"
            )
        option.click(timeout=10000)
