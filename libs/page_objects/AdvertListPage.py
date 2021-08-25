import time

from PageObjectLibrary import PageObject
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import re
from common import *
from current_env import *


class AdvertListPage(PageObject):
    IS_DYNAMIC = True
    PAGE_URL = "/%s/quang-cao?lang=%s"

    def _is_current_page(self):
        location = self.se2lib.get_location()
        regex_match = G_root_url.replace('/','\\/') + '\\d+'  '\/quang-cao.*$'
        template = re.compile(r'{}'.format(regex_match))
        if template.match(location) is None:
            message = "Expected location match with " + regex_match + " but it did not\n" \
                                                                       "current location is: " + location
            raise Exception(message)
        return True

    _locators = {
        "campaign_name":                "css=#main-page-content .campaign-name .edit-wrapper .orange-text",
        "campaign_status":              "(//*[@id='main-page-content']//div[contains(@class,'campaign-items')]//div[@class='item-row'])[2]//div[contains(text(),'Trạng thái') or contains(text(),'Status')]//span[@data-status]",
        "campaign_type":                "(//*[@id='main-page-content']//div[contains(@class,'campaign-items')]//div[@class='item-row'])[2]//div[contains(text(),'Loại hình') or contains(text(),'Type')]//b",
        "campaign_from":                "//*[@id='campaign_period']/strong[1]",
        "campaign_to":                  "//*[@id='campaign_period']/strong[2]",
        "campaign_delivery_type":       "(//*[@id='main-page-content']//div[contains(@class,'campaign-items')]//div[@class='item-row'])[2]//div[contains(text(),'Loại phân phối') or contains(text(),'Delivery type')]//strong//span",
        "campaign_daily_limit":         "(//*[@id='main-page-content']//div[contains(@class,'campaign-items')]//div[@class='item-row'])[3]//div[contains(text(),'Giới hạn ngày') or contains(text(),'Daily limit')]//strong//span",
        "campaign_stats_tracking":      "(//*[@id='main-page-content']//div[contains(@class,'campaign-items')]//div[@class='item-row'])[4]//div[contains(text(),'Theo dõi thống kê') or contains(text(),'Stat tracking')]//span[contains(@class,'bold')]",
        "campaign_payment_type":        "(//*[@id='main-page-content']//div[contains(@class,'campaign-items')]//div[@class='item-row'])[4]//div[contains(text(),'Phương thức tính phí') or contains(text(),'Payment type')]//strong",

    }

    def get_campaign_all_info(self):
        """
        get all information of current campaign in campaign list
        :return:
        Dictionary
        """
        map_dict = {
            "campaign_name": self.locator.campaign_name,
            "campaign_status": self.locator.campaign_status,
            "campaign_type": self.locator.campaign_type,
            "campaign_from": self.locator.campaign_from,
            "campaign_to": self.locator.campaign_to,
            "campaign_delivery_type": self.locator.campaign_delivery_type,
            "campaign_daily_limit": self.locator.campaign_daily_limit,
            "campaign_stats_tracking": self.locator.campaign_stats_tracking,
            "campaign_payment_type": self.locator.campaign_payment_type
        }
        campaign_infor = {}
        for key in map_dict:
            locator = map_dict[key]
            try:
                key_infor = get_element_attribute_with_retry(locator, 'textContent').strip().replace('\n','').replace('\t','').replace('\s+',' ')
                campaign_infor[key] = key_infor
            except Exception as e:
                print(e)
                campaign_infor[key] = None

        return campaign_infor


if __name__=='__main__':
    print(G_root_url.replace('/','\\/'))