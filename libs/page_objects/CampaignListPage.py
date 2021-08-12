from PageObjectLibrary import PageObject
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import re


class CampaignListPage(PageObject):
    IS_DYNAMIC = True
    PAGE_URL = "/campaign/negative-phrase/%s"

    _locators = {

    }

    def _is_current_page(self):
        location = self.se2lib.get_location()
        template_str = '.*' + self.PAGE_URL.replace('%s', '.*') + '$'
        regex_match = ''
        for character in template_str[2:-3]:
            if re.match(r'[[\]()/*+?,\\^$|#\\|]', character):
                regex_match += '\\' + character
            else:
                regex_match += character
        template = re.compile(r'%s' % '.*' + regex_match + '.*$')
        if template.match(location) is None:
            message = "Expected location to end with " + \
                      template_str + " but it did not"
            raise Exception(message)
        return True
