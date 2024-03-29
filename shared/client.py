import os
from os import getcwd, path

from playwright.sync_api import sync_playwright, Browser, Playwright, Page

from shared.config.config import shared_config


class SharedClient:
    BASE_URL = shared_config['base-url']
    BROWSER_NAME = 'chromium'
    BROWSER_CONFIG = dict(headless=False, slow_mo=50)
    browser: Browser = None
    page: Page = None
    playwright: Playwright
    is_closed = False

    @classmethod
    def open_browser(cls):
        playwright = sync_playwright().start()
        kwargs = cls.BROWSER_CONFIG or {}
        browser_type = getattr(playwright, cls.BROWSER_NAME)
        cls.browser = browser_type.launch(**kwargs)
        # dump local storage file with token.
        state_file = shared_config['storage-dump']
        # check if dump exists and make flag = true.
        if os.path.exists(state_file):
            context = cls.browser.new_context(ignore_https_errors=True,
                                              storage_state=state_file)
            cls.IS_LOGGED = True
        else:
            video_path = path.join(getcwd(), '../..', shared_config['test-results-folder'], 'allure-results')
            context = cls.browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080},
                                              record_video_dir=video_path,
                                              record_video_size={'width': 960, 'height': 680})
        cls.playwright = playwright
        cls.browser = context.browser
        cls.page = context.new_page()

    @classmethod
    def close(cls):
        if cls.is_closed:
            return
        cls.browser.close()
        cls.playwright.stop()
        cls.is_closed = True

    @classmethod
    def go_to(cls, url):
        cls.page.goto(url)

    @classmethod
    def take_screenshot(cls):
        # screenshot_path = path.join(getcwd(), '../..', shared_config['test-results-folder'], 'allure-results', 'screenshot.png')
        screenshot_path = path.join(getcwd(), '../..', 'allure-results', 'screenshot.png')
        cls.page.screenshot(path=screenshot_path)
