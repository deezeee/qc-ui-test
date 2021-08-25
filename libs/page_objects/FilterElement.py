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
        "add_filter_btn":               ".filter-panel .filter-list .add-button",
        "filter_operator_cnt":          "//*[@class='filter-panel']//div[@class='operator']",
        "add_filter_operator_btn":      "(//*[@class='filter-panel']//div[@class='operator'])[${replace}]",
    }

    def add_filter(self, filter_group, filter_type, value, operator=None):
        """
            add filter in any page contain this component,
            Group 1: filter kind of just select value from multi-select dropdown ex: Type
                     value should be list to multi-select
            Group 2: filter select operator and input value ex: ID need input operator (= > < ...)
                     if filter_type == in_range: value should be list contains 2 values [from, to]
        """
        self.select_filter_type(filter_type)

        if int(filter_group) == 1:
            for val in value:
                real_locator = self.locator.cl_filter_multi_select_dropdown.replace('${CL_FILTER_MULTI_SELECT_DROPDOWN}', str(val))
                click_element_using_mouse_event(real_locator)
        elif int(filter_group) == 2:
            self.select_cl_filter_operator_value(operator)
            self.input_cl_filter_number_value(value)

        self.click_cl_filter_apply_button()
        self.wait_for_processing()

    def click_add_filter_button(self):
        """
            click add filter button
        """
        add_filter_btn = self.locator.add_filter_btn
        click_element_using_mouse_event(add_filter_btn)

    def click_add_filter_operator_button(self, filter_name):
        """
            click operator button in adding filter
        """
        self.se2lib.get_element_count()
        adding_filter_operator_btn = self.locator.cl_operator_select
        click_element_using_mouse_event(real_locator)

    def click_cl_columns_icon(self):
        """
            Click `COLUMNS` icon to add more column to show in table
        """
        real_locator = self.locator.cl_column_plus
        click_element_using_mouse_event(real_locator)

    def click_cl_filter_apply_button(self):
        """
            click apply button on filter bar
        """
        real_locator = self.locator.cl_filer_apply
        click_element_using_mouse_event(real_locator)

    def remove_cl_filter_all_filter(self):
        """
            click `x` button to remove all filter in campaign list filter
        """
        x_locator = self.locator.cl_remove_filter.replace('[${CL_REMOVE_FILTER}]', '')
        number_of_filter = int(self.se2lib.get_element_count(x_locator))
        real_locator = self.locator.cl_remove_filter.replace('${CL_REMOVE_FILTER}', '1')
        for index in range(1, number_of_filter + 1):
            click_element_using_mouse_event(real_locator)
        self.se2lib.wait_until_element_is_not_visible(real_locator)

    def remove_cl_filter_by_type(self, _type):
        """
            remove filter by type of filter ex: ID, Type,...
        """
        real_locator = self.locator.cl_remove_filter_by_type.replace('${CL_REMOVE_FILTER_BY_TYPE}', str(_type))
        click_element_using_mouse_event(real_locator)
        self.wait_for_processing()