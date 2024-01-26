from shared.logger.logger import get_logger
from shared.client import SharedClient

log = get_logger(__name__)


class PageCommon:

    client = SharedClient()

    @classmethod
    def click_on_login_button(cls):
        log.info('Click on Log in button')
        cls.client.page.get_by_text('Log in').click()

    @classmethod
    def fill_email_field(cls, email: str):
        log.info(f'Fill email field: {email}')
        cls.client.page.locator('#login').fill(email)

    @classmethod
    def fill_password_field(cls, password: str):
        log.info(f'Fill password field: {password}')
        cls.client.page.locator("#password").fill(password)

    @classmethod
    def click_on_sign_in_button(cls):
        log.info(f'Click on Sign in button')
        cls.client.page.locator('.big-button.b-w.jsLogIn').click()

    @classmethod
    def get_login_error_text(cls):
        log.info('Get error text')
        cls.client.page.wait_for_selector('#iloginRejectReason')
        error_text = cls.client.page.locator('#iloginRejectReason').text_content()
        return error_text

    @classmethod
    def make_screenshot(cls):
        screenshot = cls.client.page.screenshot(type='png', path='screenshot.png')
        return screenshot
