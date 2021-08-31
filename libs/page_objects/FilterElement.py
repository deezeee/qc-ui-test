import robot.api
from robot.api import logger
from PageObjectLibrary.locatormap import LocatorMap
from robot.libraries.BuiltIn import BuiltIn
from contextlib import contextmanager
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from common import *


class FilterElement:

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
        self.se2lib.wait_for_condition("return (document.readyState == 'complete')", timeout=timeout)

    _locators = {
        "add_filter_btn":               "css=.filter-panel .filter-list .add-button",
        "filter_by_name":               "//*[@class='filter-panel']//div[@class='field' and text()='${replace}']",
        "filter_dropdown":              "//*[contains(@class,'dropdown-component')]//span[text()='${replace}']",
        "filter_operator_sub_fix":      "//following-sibling::div[@class='operator']//option[@value='${replace}']",
        "filter_apply_btn":             "//*[@class='filter-panel']//button[@class='apply-button']",
        "filter_remove_btn_by_name":    "//*[@class='filter-panel']//div[@class='field' and text()='${replace}']/ancestor::div[@class='filter-wrapper']//button[@class='remove-button']",
        "process_popup":                "//*[@class='ajax-shield-wrapper']//span[text()]",
        "filter_string_value_subfix":   "//following-sibling::div[@class='value']//input",
        "filter_remove_btn":            "(//*[@class='filter-panel']//button[@class='remove-button'])",
    }

    def wait_for_processing(self, timeout=30):
        """
        Wait for loading after apply filter
        :return: None
        """
        try:
            self.se2lib.wait_until_page_contains_element(self.locator.process_popup, 1)
        except Exception as e:
            print(e)
            pass
        self.se2lib.wait_until_page_does_not_contain_element(self.locator.process_popup, timeout)
        time.sleep(1)

    def add_filter(self, filter_group, filter_type, operator, values):
        """
        Add filter in any page contain this component,
        :param filter_group: Number [1 or 2]
            Group '1': filter that just select value from multi-select dropdown ex: Type
                     value should be list to multi-select
            Group '2': filter that select operator and input value ex: ID need input operator (= > < ...)
                     if filter_type == in_range: value should be list contains 2 values [from, to]
        :param filter_type: ID/Status/Campaign/...
        :param values:
            if group = 1: List contains values that you want to select ['Search Banner', 'Search Ads', ...]
            if group = 2:
                operator = in_range: List contains 2 values ['from', 'to']
                in_range = in_list: List
                else: String
        :param operator: String
            =, >, <, <=, >=,
            in_list, in_range, contain, not_contain,
            start_with, not_start_with,
            end_with, not_end_with
        :return: None
        """
        self.select_filter_type(filter_type)

        if int(filter_group) == 1:
            for val in values:
                value_locator = self.locator.filter_dropdown.replace('${replace}', str(val))
                click_element_using_mouse_event(value_locator)
        elif int(filter_group) == 2:
            self.click_operator_button_in_filter_by_name(filter_type)
            self.select_filter_operator_value(filter_type, operator)
            if operator == 'in_list':
                self.input_filter_in_list_value(filter_type, values)
            elif operator == 'in_range':
                print('ABC')
                self.input_filter_in_range_value(filter_type, values)
            else:
                self.input_filter_string_value(filter_type, values)

        self.click_filter_apply_button()
        self.wait_for_processing()

    def click_to_added_filter_by_name(self, filter_name):
        """
        Click to added filter to open this filter to edit
        :param filter_name: String
        :return: None
        """
        current_filter = self.locator.filter_by_name.replace('${replace}', filter_name)
        click_element(current_filter)

    def click_add_filter_button(self):
        """
        Click Add filter button
        :return: None
        """
        add_filter_btn = self.locator.add_filter_btn
        click_element_using_mouse_event(add_filter_btn)

    def select_filter_type(self, filter_type):
        """
        Select filter by given type
        :param type: String
        :return: None
        """
        self.click_add_filter_button()
        filter_dropdown = self.locator.filter_dropdown.replace('${replace}', filter_type)
        click_element_using_mouse_event(filter_dropdown)

    def click_operator_button_in_filter_by_name(self, filter_name):
        """
        Click operator button in adding filter
        :param filter_name: filter name ex: ID/Status, ...
        :return: None
        """
        # this step is used for edit filter
        self.click_to_added_filter_by_name(filter_name)

        current_filter = self.locator.filter_by_name.replace('${replace}', filter_name)
        add_operator_btn = current_filter + "/parent::div//select"
        click_element(add_operator_btn)

    def select_filter_operator_value(self, filter_name, operator):
        """
        Select operator of filter that contain operator
        :param operator: String
            =, >, <, <=, >=,
            in_list, in_range, contain, not_contain,
            start_with, not_start_with,
            end_with, not_end_with
        :return: None
        """
        filter_operator_value = self.locator.filter_by_name.replace('${replace}', filter_name) \
                              + self.locator.filter_operator_sub_fix.replace('${replace}', operator)
        click_element(filter_operator_value)

    def input_filter_string_value(self, filter_name, value):
        """
        Input to filter value with operator is not in_range or in_list
        :param filter_name: String
        :param value: String
        :return: None
        """
        # this step is used for edit filter
        self.click_to_added_filter_by_name(filter_name)

        current_filter = self.locator.filter_by_name.replace('${replace}', filter_name)
        current_filter_input = current_filter + self.locator.filter_string_value_subfix
        input_text_with_retry(current_filter_input, value)

    def input_filter_in_range_value(self, filter_name, values):
        """
        Input to filter value with operator is in_range
        :param filter_name: String
        :param value: List [from, to]
        :return: None
        """
        if not isinstance(values, list):
            return
        # this step is used for edit filter
        self.click_to_added_filter_by_name(filter_name)

        current_filter = self.locator.filter_by_name.replace('${replace}', filter_name)
        current_filter_input_from = current_filter + self.locator.filter_string_value_subfix + '[1]'
        current_filter_input_to = current_filter + self.locator.filter_string_value_subfix + '[2]'
        input_text_with_retry(current_filter_input_from, str(values[0]))
        input_text_with_retry(current_filter_input_to, str(values[1]))

    def input_filter_in_list_value(self, filter_name, values):
        """
        Input to filter value with operator is in_list
        :param filter_name: String
        :param value: List of String
        :return: None
        """
        if not isinstance(values, list):
            return
        # this step is used for edit filter
        self.click_to_added_filter_by_name(filter_name)

        current_filter = self.locator.filter_by_name.replace('${replace}', filter_name)
        current_filter_input = current_filter + self.locator.filter_string_value_subfix
        values = ','.join(values)
        input_text_with_retry(current_filter_input, values)

    def click_filter_apply_button(self):
        """
        Click apply button when add filter
        :return: None
        """
        apply_btn = self.locator.filter_apply_btn
        click_element(apply_btn)

    def remove_filter_by_name(self, filter_name):
        """
        Remove filter by given filter name
        :param filter_name: String
        :return: None
        """
        remove_filter_button = self.locator.filter_remove_btn_by_name.replace('${replace}', filter_name)
        click_element(remove_filter_button)

    def remove_all_filters(self):
        """
        Remove all added filters
        :return: None
        """
        total_filters = self.locator.filter_remove_btn
        number_of_filters = self.se2lib.get_element_count(total_filters)
        for i in range(0, number_of_filters):
            remove_btn = total_filters + '[1]'
            click_element(remove_btn)
            self.wait_for_processing()
