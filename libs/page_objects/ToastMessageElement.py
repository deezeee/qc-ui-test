import robot.api
from robot.api import logger
from PageObjectLibrary.locatormap import LocatorMap
from robot.libraries.BuiltIn import BuiltIn
from contextlib import contextmanager
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait


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
    }
