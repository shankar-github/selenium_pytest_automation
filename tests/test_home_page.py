import pytest

from pages.home_page import MagentoHomePage
from utils.config import PAGE_LOAD_TIME
from utils.logger import get_logger

# Get logger instance
logger = get_logger(__name__)


@pytest.mark.parametrize(
    "search_query",
    ["shirt"]
)
def test_search_product(start_browser, search_query):
    logger.info(f"Starting test_search_product with search query: {search_query}")
    browser = start_browser
    magento_home = MagentoHomePage(browser, PAGE_LOAD_TIME)
    search_results = magento_home.search_for_product(search_query)
    # Assert that search results are displayed
    assert search_results.are_search_results_displayed(), "Search results are not displayed"
    logger.info("Search results are displayed successfully.")


# def test_open_account_menu(start_browser):
#     logger.info("Starting test_open_account_menu")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.open_account_menu()
#     # Assert that account menu is opened
#     assert magento_home.is_account_menu_opened(), "Account menu is not opened"
#     logger.info("Account menu is opened successfully.")
#
#
# def test_open_cart(start_browser):
#     logger.info("Starting test_open_cart")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.open_cart()
#     # Assert that cart is opened
#     assert magento_home.is_cart_opened(), "Cart is not opened"
#     logger.info("Cart is opened successfully.")
#
#
# def test_open_my_wishlist(start_browser):
#     logger.info("Starting test_open_my_wishlist")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.open_my_wishlist()
#     # Assert that wishlist is opened
#     assert magento_home.is_wishlist_opened(), "Wishlist is not opened"
#     logger.info("Wishlist is opened successfully.")
#
#
# def test_open_compare_products(start_browser):
#     logger.info("Starting test_open_compare_products")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.open_compare_products()
#     # Assert that compare products page is opened
#     assert magento_home.is_compare_products_opened(), "Compare products page is not opened"
#     logger.info("Compare products page is opened successfully.")
#
#
# @pytest.mark.parametrize(
#     "language_code",
#     ["fr_FR", "de_DE", "es_ES"]
# )
# def test_change_language(start_browser, language_code):
#     logger.info(f"Starting test_change_language with language code: {language_code}")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.change_language(language_code)
#     # Assert that language is changed
#     assert magento_home.get_current_language() == language_code, f"Language is not changed to {language_code}"
#     logger.info("Language changed successfully.")
#
#
# @pytest.mark.parametrize(
#     "currency_code",
#     ["EUR", "GBP", "JPY"]
# )
# def test_change_currency(start_browser, currency_code):
#     logger.info(f"Starting test_change_currency with currency code: {currency_code}")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.change_currency(currency_code)
#     # Assert that currency is changed
#     assert magento_home.get_current_currency() == currency_code, f"Currency is not changed to {currency_code}"
#     logger.info("Currency changed successfully.")
#
#
# def test_navigate_slider_next(start_browser):
#     logger.info("Starting test_navigate_slider_next")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.navigate_slider_next()
#     # Add assertions here
#     logger.info("Slider navigated to the next item successfully.")
#
#
# def test_navigate_slider_previous(start_browser):
#     logger.info("Starting test_navigate_slider_previous")
#     browser = start_browser
#     magento_home = MagentoHomePage(browser)
#     magento_home.navigate_slider_previous()
#     # Add assertions here
#     logger.info("Slider navigated to the previous item successfully.")
