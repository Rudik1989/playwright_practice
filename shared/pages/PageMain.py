from shared.pages.PageCommon import PageCommon
from shared.logger.logger import get_logger

log = get_logger(__name__)


class PageMain(PageCommon):

    def navigate_to_main_page(self):
        log.info('Go to main page')
        self.page.goto("https://www.4shared.com/")
