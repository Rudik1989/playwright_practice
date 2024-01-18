from hamcrest import equal_to, assert_that

from shared.pages.PageCommon import PageCommon


class TestMainPage:

    def test_empty_login_error(self, browser):
        page_common = PageCommon(browser)
        page_common.click_on_login_button()
        page_common.click_on_sign_in_button()
        assert_that(page_common.get_login_error_text(), equal_to('Empty login1'), "Wrong error is shown")
