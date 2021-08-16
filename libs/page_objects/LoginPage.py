from PageObjectLibrary import PageObject
from common import *


class LoginPage(PageObject):
    IS_DYNAMIC = True
    PAGE_URL = "/user/login?lang=%s"

    _locators = {
        "username": "name=email",
        "password": "name=password",
        "submit_button": "xpath=//*[@id=\"client-login\"]/form/button",
        "process_popup": "//*[@class=\"ajax-shield-wrapper\"]//span[text()]",
    }

    def _is_current_page(self):
        location = self.se2lib.get_location()
        template_str = '.*' + self.PAGE_URL.replace('%s', '.*') + '$'
        regex_match = ''
        for character in template_str[2:-3]:
            if character in "[\]()/*+?,\\^$|#\\|":
                regex_match += '\\' + character
            else:
                regex_match += character
        template = re.compile(r'%s' % '.*' + regex_match + '.*$')
        if template.match(location) is None:
            message = "Expected location to end with " + \
                      template_str + " but it did not"
            raise Exception(message)
        return True

    def enter_username(self, username):
        """Type the given text into the username field """
        input_text_with_retry(self.locator.username, username)

    def enter_password(self, password):
        """Type the given text into the password field"""
        input_text_with_retry(self.locator.password, password)

    def click_the_login_button(self, wait_refresh='true'):
        """Click the submit button, and wait for the page to reload"""
        if wait_refresh == 'true':
            with self._wait_for_page_refresh():
                click_element_using_mouse_event(self.locator.submit_button)
            self.se2lib.wait_until_page_does_not_contain_element(self.locator.process_popup, timeout=120)
        else:
            click_element_using_mouse_event(self.locator.submit_button)
