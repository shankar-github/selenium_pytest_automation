from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

# Get logger instance
from pages.search_results_page import SearchResultPage
from utils.config import PAGE_LOAD_TIME

logger = get_logger(__name__)


class MagentoHomePage(BasePage):
    # Locators
    _search_input = (By.ID, "search")
    _search_button = (By.XPATH, "//button[@title='Search']")
    _account_link = (By.XPATH, "//a[@data-action='customer-menu-toggle']")
    _cart_link = (By.XPATH, "//a[@class='action showcart']")
    _my_wishlist_link = (By.XPATH, "//a[@id='wishlist-link']")
    _compare_products_link = (By.XPATH, "//a[@id='compare-products-link']")
    _language_dropdown = (By.XPATH, "//div[@data-block='store-language']//button")
    _currency_dropdown = (By.XPATH, "//div[@data-block='store-currency']//button")
    _slider_next_button = (By.XPATH, "//button[@class='action next']")
    _slider_previous_button = (By.XPATH, "//button[@class='action prev']")

    def __init__(self, driver, time_out):
        super().__init__(driver)
        self.driver = driver
        self.timeout = time_out

    # Private methods to interact with elements
    def _search(self, query):
        self.type_text(self._search_input, query)
        self.click_element(self._search_button)
        logger.info(f"Searched for product: {query}")

    def _click_account_link(self):
        self.click_element(self._account_link)
        logger.info("Clicked on the account link")

    def _click_cart_link(self):
        self.click_element(self._cart_link)
        logger.info("Clicked on the cart link")

    def _click_my_wishlist_link(self):
        self.click_element(self._my_wishlist_link)
        logger.info("Clicked on the my wishlist link")

    def _click_compare_products_link(self):
        self.click_element(self._compare_products_link)
        logger.info("Clicked on the compare products link")

    def _select_language(self, language):
        self.click_element(self._language_dropdown)
        language_locator = (By.XPATH, f"//a[@data-store-code='{language}']")
        self.click_element(language_locator)
        logger.info(f"Changed language to: {language}")

    def _select_currency(self, currency):
        self.click_element(self._currency_dropdown)
        currency_locator = (By.XPATH, f"//a[@data-currency-code='{currency}']")
        self.click_element(currency_locator)
        logger.info(f"Changed currency to: {currency}")

    def _click_slider_next(self):
        self.click_element(self._slider_next_button)
        logger.info("Clicked on the next slider button")

    def _click_slider_previous(self):
        self.click_element(self._slider_previous_button)
        logger.info("Clicked on the previous slider button")

    # Public methods to expose functionality to test class
    def search_for_product(self, product_name):
        """
        Search for a product using the search input field.
        """
        self._search(product_name)
        return SearchResultPage(self._driver, PAGE_LOAD_TIME)

    def open_account_menu(self):
        """
        Open the account menu.
        """
        self._click_account_link()
        logger.info("Opened the account menu")

    def open_cart(self):
        """
        Open the cart.
        """
        self._click_cart_link()
        logger.info("Opened the cart")

    def open_my_wishlist(self):
        """
        Open my wishlist.
        """
        self._click_my_wishlist_link()
        logger.info("Opened my wishlist")

    def open_compare_products(self):
        """
        Open the compare products page.
        """
        self._click_compare_products_link()
        logger.info("Opened the compare products page")

    def change_language(self, language_code):
        """
        Change the language of the website.
        """
        self._select_language(language_code)
        logger.info(f"Changed language to: {language_code}")

    def change_currency(self, currency_code):
        """
        Change the currency of the website.
        """
        self._select_currency(currency_code)
        logger.info(f"Changed currency to: {currency_code}")

    def navigate_slider_next(self):
        """
        Navigate to the next slide in the slider.
        """
        self._click_slider_next()
        logger.info("Navigated to the next slide in the slider")

    def navigate_slider_previous(self):
        """
        Navigate to the previous slide in the slider.
        """
        self._click_slider_previous()
        logger.info("Navigated to the previous slide in the slider")
