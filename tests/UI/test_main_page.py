from hamcrest import equal_to, assert_that

from shared.pages.PageCommon import PageCommon


class TestMainPage:

    def test_empty_login_error(self, open_browser):
        PageCommon.click_on_login_button()
        PageCommon.click_on_sign_in_button()
        assert_that(PageCommon.get_login_error_text(), equal_to('Empty login1'), "Wrong error is shown")

    def test_empty_login_error1(self, open_browser):
        PageCommon.click_on_login_button()
        PageCommon.click_on_sign_in_button()
        assert_that(PageCommon.get_login_error_text(), equal_to('Empty login'), "Wrong error is shown")


