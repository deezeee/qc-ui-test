import robot.api
from robot.api import logger
from PageObjectLibrary.locatormap import LocatorMap
from robot.libraries.BuiltIn import BuiltIn
from contextlib import contextmanager
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from common import *


class ToastMessageElement:

    def __init__(self):
        self.logger = robot.api.logger
        self.locator = LocatorMap(getattr(self, "_locators", {}))

    @property
    def se2lib(self):
        return BuiltIn().get_library_instance("Selenium2Library")

    @property
    def browser(self):
        return self.se2lib._current_browser()

    def __str__(self):
        return self.__class__.__name__

    def get_page_name(self):
        """Return the name of the current page """
        return self.__class__.__name__

    @contextmanager
    def _wait_for_page_refresh(self, timeout=10):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page),
            message="Old page did not go stale within %ss" % timeout
        )
        self.se2lib.wait_for_condition("return (document.readyState == 'complete')", timeout=10)

    _locators = {
        "toast_container":              "css=.toasts-container",
        "success_toast":                "css=.toasts-container .toast-success",
        "warning_toast":                "css=.toasts-container .toast-warning",
        "error_toast":                  "css=.toasts-container .toast-error",
        "toast_message":                "css=.toasts-container .toast .message div",
        "remove_toast_btn":             "css=.toasts-container .toast button.remove-button"
    }

    def close_toast_message(self):
        """
        Click x button to close toast message
        :return: None
        """
        close_btn = self.locator.remove_toast_btn
        toast_container = self.locator.toast_container
        self.se2lib.wait_until_element_is_visible(toast_container, timeout=1)
        click_element(close_btn)
        self.se2lib.wait_until_element_is_not_visible(toast_container, timeout=1)


    def page_should_contain_success_toast_message(self, message):
        """
        wait for page contain success toast message
        :param message: String (Expected message)
        :return: Boolean
        """
        toast_container = self.locator.toast_container
        success_toast = self.locator.success_toast
        green_color = "#67B458"

        self.se2lib.wait_until_element_is_visible(toast_container, timeout=1)
        color = get_element_css_style_value(success_toast, "color")

        toast_message = self.locator.toast_message
        show_message = get_element_attribute_with_retry(toast_message, "textContent")

        if color==green_color and show_message==message:
            return True

        return False

    def page_should_contain_error_toast_message(self, message):
        """
        wait for page contain error toast message
        :param message: String (Expected message)
        :return: Boolean
        """
        toast_container = self.locator.toast_container
        error_toast = self.locator.error_toast
        red_color = "#EF5858"

        self.se2lib.wait_until_element_is_visible(toast_container, timeout=1)
        color = get_element_css_style_value(error_toast, "color")

        toast_message = self.locator.toast_message
        show_message = get_element_attribute_with_retry(toast_message, "textContent")

        if color==red_color and show_message==message:
            return True

        return False
