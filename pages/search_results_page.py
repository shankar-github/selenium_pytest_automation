from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

from utils.config import PAGE_LOAD_TIME

logger = get_logger(__name__)


class SearchResultPage(BasePage):
    # Locators
    _search_results = (By.XPATH, "//div[@class='search results']")

    def __init__(self, driver, time_out):
        super().__init__(driver)
        self.driver = driver
        self.timeout = time_out

    # Private methods to interact with elements
    def _get_search_results(self):
        return self.is_element_present(self._search_results)

    # Public methods
    def are_search_results_displayed(self):
        return self._get_search_results()
