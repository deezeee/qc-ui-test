from PageObjectLibrary import PageObject
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import re
from common import *
from current_env import *


class CampaignListPage(PageObject):
    IS_DYNAMIC = True
    PAGE_URL = "/chien-dich/%s&lang=%s"

    def _is_current_page(self):
        location = self.se2lib.get_location()
        template_str = G_root_url + 'chien-dich/.*$'
        regex_match = ''
        for character in template_str[0:-3]:
            if character in "[\]()/*+?,\\^$|#\\|":
                regex_match += '\\' + character
            else:
                regex_match += character
        print(regex_match)
        template = re.compile(r'%s' % regex_match)
        if template.match(location) is None:
            message = "Expected location match with " + template_str + " but it did not\n" \
            "current location is: " + location
            raise Exception(message)
        return True

    _locators = {
        "create_campaign_button":               "css=#campaign-list-app-root .main-actions button",
        "magic_panel":                          "css=div.float-panel.open",
        "placement_type_btn":                   "//*[@id='qc4-migration']//div[@data-field='placement_type']//li//div[@class='name' and text()='${replace}']",
        "placement_position_btn":               "//*[@id='qc4-migration']//div[@data-field='placement_position']//li//div[@class='label' and text()='${replace}']",
        "campaign_type_btn":                    "//*[@id='qc4-migration']//div[@data-field='campaign_type']//li//div[@class='label' and text()='${replace}']",
        "create_campaign_form_btn":             "(//*[@class='campaign-create-panel']//div[@class='custom-form__actions']//button)[2]",
        "discard_create_form_btn":              "(//*[@class='campaign-create-panel']//div[@class='custom-form__actions']//button)[1]",
        "campaign_name_input":                  "css=.campaign-create-panel .custom-form__content [data-field=name] input",
        "campaign_name_error":                  "css=.campaign-create-panel .custom-form__content [data-field=name] .field-error div",
        "date_from":                            "//*[@class='date-to-date-input']//div[contains(@class,'date-input')][1]//ul//li[1]//input",
        "date_to":                              "//*[@class='date-to-date-input']//div[contains(@class,'date-input')][2]//ul//li[1]//input",
        "daily_limit":                          "//*[@data-field='daily_limit_type']//div[@class='selection']",
        "daily_limit_by_budget":                "//*[@data-field='spendings_daily_limit']//input",
        "daily_limit_by_budget_error":          "//*[@data-field='spendings_daily_limit']//div[@class='field-error']//div[text()]",
        'daily_limit_by_impressions':           "//*[@data-field='impression_daily_limit']//input",
        'daily_limit_by_impressions_error':     "//*[@data-field='impression_daily_limit']//div[@class='field-error']//div[text()]",
        "delivery_standard":                    "//*[@data-field='ad_delivery']//li[1]",
        "delivery_accelerated":                 "//*[@data-field='ad_delivery']//li[2]",
        "stats_tracking_on":                    "//*[@data-field='tracking_enabled']//li[1]",
        "stats_tracking_off":                   "//*[@data-field='tracking_enabled']//li[2]",
        "drop_down_create":                     "//*[contains(@class,'single-select-dropdown')]//li[text()='${replace}']",
        "process_popup":                        "//*[@class='ajax-shield-wrapper']//span[text()]",
        'maximum_bid':                          '//*[@data-field="bid_strategy"]/../following-sibling::div//input',
        'maximum_bid_error':                    '//*[@data-field="bid"]//div[@class="field-error"]',
        'max_impressions_by_user':              '//*[@data-field="is_user_impressions_limited"]//div[@class="selection"]',
        'max_impressions_by_user_limited':      '//*[@data-field="shows_per_user"]//input',
        'max_impressions_period':               '//*[@data-field="shows_per_user_period"]//div[@class="selection"]',
        'max_impressions_by_user_error':        '//*[@data-field="shows_per_user"]//div[@class="field-error"]'
    }

    def wait_for_page_loading_campaign(self, timeout=120):
        """
            Wait for process done!
        """
        try:
            self.se2lib.wait_until_page_contains_element(self.locator.process_popup, 1)
        except Exception as e:
            print(e)
            pass
        self.se2lib.wait_until_page_does_not_contain_element(self.locator.process_popup, timeout)
        time.sleep(0.5)

    def click_create_campaign_button(self):
        """
            Click to "CREATE CAMPAIGN BUTTON"
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
        campaign_type_btn = self.locator.campaign_type_btn.replace('${replace}', campaign_type)
        wait_until_element_is_visible_and_click_element(campaign_type_btn)

    def input_campaign_name(self, name):
        """
            Input `name` to `Campaign Name` field
        """
        input_text_with_retry(self.locator.campaign_name_input, name)

    def input_campaign_period(self, date_from, date_to):
        """
            Input date to `Period` field
            date_from and date_to must in format:
            dd/mm/yyyy
        """
        if date_to != None:
            to_locator = self.locator.date_to
            date_to = date_to.replace('/', '')
            self.se2lib.wait_until_element_is_visible(to_locator)
            self.se2lib.press_key(to_locator, date_to)
            self.se2lib.press_key(to_locator, '\\13')
        if date_from != None:
            from_locator= self.locator.date_from
            date_from = date_from.replace('/', '')
            self.se2lib.wait_until_element_is_visible(from_locator)
            self.se2lib.press_key(from_locator, date_from)
            self.se2lib.press_key(from_locator, '\\13')

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
            real_from_locator = self.locator.date_from.replace('${replace}', str(index))
            val = get_element_attribute_with_retry(real_from_locator, 'value')
            date_from += str(val) + '/'

            real_to_locator = self.locator.date_to.replace('${replace}', str(index))
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
        daily_limit_type = self.se2lib.get_element_attribute(self.locator.daily_limit, 'textContent')
        if daily_limit_type == 'By budget' or daily_limit_type == 'Theo ngân sách':
            input_number_to_qc(self.locator.daily_limit_by_budget, daily_limit)
        elif daily_limit_type == 'By impressions' or daily_limit_type == 'Theo lượt hiển thị':
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

    def get_error_message_of_field(self, field):
        """
            -use for getting error messages.
            -field should be (lower case or upper case doesn't matter):
                campaign name
                maximum bid
                daily limit by budget
                daily limit by impressions
                max impressions by user
        """
        error_field = {
            'campaign name': self.locator.campaign_name_error,
            'maximum bid': self.locator.maximum_bid_error,
            'daily limit by budget': self.locator.daily_limit_by_budget_error,
            'daily limit by impressions': self.locator.daily_limit_by_impressions_error,
            'max impressions by user': self.locator.max_impressions_by_user_error
        }
        try:
            self.se2lib.wait_until_element_is_visible(error_field[field.lower()], 0.2)
            return get_element_attribute_with_retry(error_field[field.lower()], 'textContent').encode('ascii', 'ignore')
        except:
            return ""

    def get_all_error_message_of_create_new_campaign(self):
        """
            get all error message on create campaign page
        """
        messages = {}
        error_field = {
            'campaign name': self.locator.campaign_name_error,
            'maximum bid': self.locator.maximum_bid_error,
            'daily limit by budget': self.locator.daily_limit_by_budget_error,
            'daily limit by impressions': self.locator.daily_limit_by_impressions_error,
            'max impressions by user': self.locator.max_impressions_by_user_error
        }
        for key in error_field:
            messages[key] = self.get_error_message_of_field(key)
        return messages

    def click_create_campaign_save_button(self, valid_data=True, timeout=25):
        """
            Click `Ceate campaign` after fill data
            valid_data = True: check redirect to other page
            else do nothing just click
        """
        if valid_data:
            with self._wait_for_page_refresh(timeout):
                click_element(self.locator.create_campaign_form_btn)
                error_messages = self.get_all_error_message_of_create_new_campaign()
            page_url = self.se2lib.get_location()
            patern = r'http.*\/(\d+)\/.*'
            match = re.search(patern, page_url)
            return match.group(1), error_messages
        else:
            click_element(self.locator.create_campaign_form_btn)


if __name__=='__main__':
    pass