from shared.logger.logger import get_logger
from playwright.sync_api import Page, Browser

log = get_logger(__name__)


class PageCommon:

    def __init__(self, browser: Browser, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()

    def click_on_login_button(self):
        log.info('Click on Log in button')
        self.page.get_by_text('Log in').click()

    def fill_email_field(self, email: str):
        log.info(f'Fill email field: {email}')
        self.page.locator('#login').fill(email)

    def fill_password_field(self, password: str):
        log.info(f'Fill password field: {password}')
        self.page.locator("#password").fill(password)

    def click_on_sign_in_button(self):
        log.info(f'Click on Sign in button')
        self.page.locator('.big-button.b-w.jsLogIn').click()

    def get_login_error_text(self):
        log.info('Get error text')
        self.page.wait_for_selector('#iloginRejectReason')
        error_text = self.page.locator('#iloginRejectReason').text_content()
        return error_text

    @classmethod
    def make_screenshot(self):
        screenshot = self.page.screenshot(type='png', path='screenshot.png')
        return screenshot
