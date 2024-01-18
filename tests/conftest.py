from playwright.sync_api import sync_playwright
import pytest

from shared.config.config import shared_config


@pytest.fixture(autouse=True, scope='function')
def browser(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        device = request.config.getoption('--device')
        if device is not None:
            context = browser.new_context(**p.devices[device])
        else:
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        base_url = request.config.getoption('--base-url')
        print(base_url)
        if base_url:  # Check if base_url is not empty
            page.goto(base_url)
        else:
            page.goto(shared_config['base-url'])
        yield page
        context.close()
        browser.close()
