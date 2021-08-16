from PageObjectLibrary import PageObject
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import re
from common import *


class CampaignListPage(PageObject):
    IS_DYNAMIC = True
    PAGE_URL = "/campaign/negative-phrase/%s"

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

    _locators = {
        "create_campaign_button":               "#campaign-list-app-root .main-actions button",
        "magic_panel":                          "div.float-panel.open",
        "placement_type_btn":                   "//*[@id='qc4-migration']//div[@data-field='placement_type']//li//div[@class='content' and text()='${replace}']",
        "placement_position_btn":               "//*[@id='qc4-migration']//div[@data-field='placement_position']//li//div[@class='label' and text()='${replace}']",
        "campaign_type_btn":                    "//*[@id='qc4-migration']//div[@data-field='campaign_type']//li//div[@class='label' and text()='${replace}']",
        "create_campaign_form_btn":             "(//*[@class='campaign-create-panel']//div[@class='campaign-form']//div[@class='form-actions']//button)[1]",
        "discard_create_form_btn":              "(//*[@class='campaign-create-panel']//div[@class='campaign-form']//div[@class='form-actions']//button)[2]",
        "campaign_name_input":                  "//*[@class='campaign-create-panel']//div[@class='campaign-form']//div[@data-field='name']//input",
        "date_from":                            "//*[@class='date-to-date-input']//div[contains(@class,'date-input')][1]//ul//li[${replace}]//input",
        "date_to":                              "//*[@class='date-to-date-input']//div[contains(@class,'date-input')][2]//ul//li[${replace}]//input",
        "daily_limit":                          "//*[@data-field='daily_limit_type']//div[@class='selection']",
        "daily_limit_by_budget":                "//*[@data-field='spendings_daily_limit']//input",
        "daily_limit_by_budget_error":          "//*[@data-field='spendings_daily_limit']//div[@class='field-error']",
        "daily_limit_by_impressions":           "//*[@data-field='impression_daily_limit']//input",
        "daily_limit_by_impressions_error":     "//*[@data-field='impression_daily_limit']//div[@class='field-error']",
        "delivery_standard":                    "//*[@data-field='ad_delivery']//li[1]",
        "delivery_accelerated":                 "//*[@data-field='ad_delivery']//li[2]",
        "stats_tracking_on":                    "//*[@data-field='tracking_enabled']//li[1]",
        "stats_tracking_off":                   "//*[@data-field='tracking_enabled']//li[2]",
        "drop_down_create":                     "//*[contains(@class,'single-select-dropdown')]//li[text()='${replace}']",
    }

    def click_create_campaign_button(self):
        """
        Click to "CREATE CAMPAIGN BUTTON"
        :return:
        """
        create_campaign_btn = self.locator.create_campaign_button
        click_element(create_campaign_btn)

        magic_panel = self.locator.magic_panel
        self.se2lib.wait_until_element_is_visible(magic_panel)

    def select_where_you_want_to_display_your_ads(self, location):
        """
            Select `Choose where you want to display your ads`
        """
        location_radio_btn = self.locator.placement_type_btn.replace('${replace}', str(location))
        click_element(location_radio_btn)

    def select_the_position_of_your_ads(self, position):
        """
            Select `Choose the position of your ads`
        """
        position_radio_btn = self.locator.placement_position_btn.replace('${replace}', str(position))
        click_element(position_radio_btn)

    def select_campaign_type(self, campaign_type):
        """
            Finally select campaign type
        """
        real_locator = self.locator.campaign_type + 'div[text()="' + campaign_type + '"]'
        wait_until_element_is_visible_and_click_element(real_locator)

    def input_campaign_name(self, name):
        """
            Input `name` to `Campaign Name` field
        """
        input_text_with_retry(self.locator.campaign_name, name)

    def input_campaign_period(self, date_from, date_to):
        """
            Input date to `Period` field
            date_from and date_to must in format:
            dd/mm/yyyy
        """
        df = date_from
        dt = date_to
        real_locator = self.locator.new_time_from.replace('${replace}', str(1))
        if not isinstance(date_from, basestring):
            date_from = str(date_from)
        date_from = date_from.replace('/', '')
        self.se2lib.wait_until_element_is_visible(real_locator)
        self.se2lib.press_key(real_locator, date_from)
        # work around
        try:
            click_element('//*[@data-field="time_period"]//div[@class="field-heading"]')
        except:
            pass

        real_locator = self.locator.new_time_to.replace('${replace}', str(1))
        if not isinstance(date_to, basestring):
            date_to = str(date_to)
        date_to = date_to.replace('/', '')
        self.se2lib.wait_until_element_is_visible(real_locator)
        self.se2lib.press_key(real_locator, date_to)
        # work around
        try:
            click_element('//*[@data-field="time_period"]//div[@class="field-heading"]')
        except:
            pass

        dff, dtt = self._get_inputted_time_period()
        self.logger.info('edit periods: from {} to {}'.format(dff, dtt))
        return dff, dtt

    def _get_inputted_time_period(self):
        """
            get inputted date time
        """
        list_index = [1, 3, 5]

        date_from = ''
        date_to = ''
        for index in list_index:
            real_from_locator = self.locator.new_time_from.replace('${replace}', str(index))
            val = get_element_attribute_with_retry(real_from_locator, 'value')
            date_from += str(val) + '/'

            real_to_locator = self.locator.new_time_to.replace('${replace}', str(index))
            val_t = get_element_attribute_with_retry(real_to_locator, 'value')
            date_to += str(val_t) + '/'

        return date_from[:-1], date_to[:-1]

    def select_daily_limit_type(self, daily_limit_type):
        """
            Select daily limit type
        """
        click_element(self.locator.daily_limit)
        self._select_drop_down_create_page(daily_limit_type)

    def _select_drop_down_create_page(self, value):
        """
            Select drop down value when any drop down is floated
        """
        real_locator = self.locator.drop_down_create.replace('${replace}', str(value))
        self.se2lib.scroll_element_into_view(real_locator)
        click_element(real_locator)

    def input_daily_limit(self, daily_limit):
        """
            Input daily limit
            By budget or By impressions
        """
        daily_limit_type = self.se2lib.get_element_attribute(self.locator.daily_limit, 'textContent').encode('ascii','ignore')
        if daily_limit_type == 'By budget':
            input_number_to_qc(self.locator.daily_limit_by_budget, daily_limit)
        elif daily_limit_type == 'By impressions':
            input_number_to_qc(self.locator.daily_limit_by_impressions, daily_limit)
        else:
            pass

    def select_delivery_type(self, delivery_type):
        """
            Select delivery type
        """
        if delivery_type.lower() == 'standard':
            click_element(self.locator.delivery_standard)
        else:
            click_element(self.locator.delivery_accelerated)

    def select_stats_tracking(self, stats_tracking):
        """
            Select stats tracking on/off
        """
        if stats_tracking.lower() == 'on':
            click_element(self.locator.stats_tracking_on)
        else:
            click_element(self.locator.stats_tracking_off)