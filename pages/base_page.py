import inspect
import os
import sys
import time
from utils.logger import get_logger

import pytest
from selenium.common import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.config import PAGE_LOAD_TIME, EXPLICIT_WAIT


class BasePage:

    def __init__(self, driver, time_out=PAGE_LOAD_TIME):
        self._driver = driver
        self._time_out = time_out
        self.logger = get_logger(__name__)

    def get_page_title(self):
        """
        Retrieves the title of the current web page.

        Returns:
            str or None: The title of the web page, or None if it cannot be retrieved.
        """
        try:
            return self._driver.title
        except WebDriverException as e:
            self.logger.error("Failed to retrieve page title:{}", e, exc_info=True)
            return None

    def wait_for_element(self, locator, timeout=EXPLICIT_WAIT, polling=0.5):
        """
        Wait for an element to be present using Fluent Wait.

        Args:
            locator (tuple): Tuple containing locator strategy and locator value.
            timeout (int): Maximum time to wait for the element to be found (default 10 seconds).
            polling (float): The sleep interval between retries (default 0.5 seconds).
        returns: element
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=polling,
                                 ignored_exceptions=(NoSuchElementException,))
            element = wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"Element found with locator: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found within specified timeout with locator: {locator}")
            raise

    def get_element(self, locator, timeout=EXPLICIT_WAIT, polling=0.5, multiple=False):
        """
        Find element using given locator.

        Args:
            locator (tuple): Tuple containing locator strategy and locator value.
            timeout (int): Maximum time to wait for the element to be found (default 10 seconds).
            polling (float): The sleep interval between retries (default 0.5 seconds).
            multiple (bool): Whether to return multiple elements (default False).

        Returns:
            WebElement or list: The found element(s).

        Raises:
            NoSuchElementException: If element is not found within the specified timeout.
        """
        try:
            elements = self.wait_for_element(locator, timeout, polling)

            if multiple:
                self.logger.info(f"Returning multiple elements with locator: {locator}")
                return elements
            else:
                if isinstance(elements, list):
                    self.logger.info(f"Returning first element of multiple elements found with locator: {locator}")
                    return elements[0]
                else:
                    self.logger.info(f"Returning single element with locator: {locator}")
                    return elements
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def is_element_present(self, locator, timeout=EXPLICIT_WAIT):
        """
        Check if an element is present on the UI within a specified timeout using get_element method.

        Args:
        - locator: Tuple (locator_strategy, locator_value) specifying the locating strategy and value of the element.
        - timeout: Maximum time to wait for the element (default is 10 seconds).

        Returns:
        - True if the element is present within the timeout, False otherwise.
        """
        try:
            # Try to get the element using get_element method with a shorter timeout
            element = self.get_element(locator, timeout)
            if element:
                self.logger.info(f"Element found with locator: {locator}")
                return True
        except NoSuchElementException:
            self.logger.info(f"Element not found with locator: {locator}")
            pass  # Element not found, continue to return False
        return False

    def click_element(self, locator, timeout=EXPLICIT_WAIT):
        """
        Click on an element identified by the given locator.

        Args:
            locator (tuple): Tuple containing locator strategy and locator value.
            timeout (int): Maximum time to wait for the element to be clickable (default 10 seconds).

        Returns:
            None

        Raises:
            NoSuchElementException: If element is not found within the specified timeout.
            TimeoutException: If element is not clickable within the specified timeout.
        """
        try:
            element = self.get_element(locator, timeout)
            element.click()
            self.logger.info(f"Clicked on element with locator: {locator}")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except TimeoutException:
            self.logger.error(f"Element not clickable within specified timeout with locator: {locator}")
            raise

    def type_text(self, locator, keys, timeout=EXPLICIT_WAIT):
        """
        Send keys to an element identified by the given locator.

        Args:
            locator (tuple): Tuple containing locator strategy and locator value.
            keys (str): The keys to be sent to the element.
            timeout (int): Maximum time to wait for the element to be visible (default 10 seconds).

        Returns:
            None

        Raises:
            NoSuchElementException: If element is not found within the specified timeout.
            TimeoutException: If element is not visible within the specified timeout.
        """
        try:
            element = self.get_element(locator, timeout)
            element.send_keys(keys)
            self.logger.info(f"Typed '{keys}' into element with locator: {locator}")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except TimeoutException:
            self.logger.error(f"Element not visible within specified timeout with locator: {locator}")
            raise

    def get_element_text(self, locator, timeout=EXPLICIT_WAIT):
        """
        Get the text of an element identified by the given locator.

        Args:
            locator (tuple): Tuple containing locator strategy and locator value.
            timeout (int): Maximum time to wait for the element to be visible (default 10 seconds).

        Returns:
            str: The text of the element.

        Raises:
            NoSuchElementException: If element is not found within the specified timeout.
            TimeoutException: If element is not visible within the specified timeout.
        """
        try:
            element = self.get_element(locator, timeout)
            text = element.text
            self.logger.info(f"Retrieved text '{text}' from element with locator: {locator}")
            return text
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except TimeoutException:
            self.logger.error(f"Element not visible within specified timeout with locator: {locator}")
            raise

    def take_screenshot(self, test_case_name=None, locator=None, timeout=10, polling=0.5):
        """
        Takes a screenshot of the current web page and saves it to a file.

        Args:
            test_case_name: Name of the test case to include in the screenshot filename.
            locator: The locator tuple (strategy, value) used to find the element before taking the screenshot (default is None).
            timeout: Maximum time to wait for the element to be found (default is 10 seconds).
            polling: The sleep interval between retries (default is 0.5 seconds).
        """
        try:
            # Compute test case name based on the caller's function name if not provided
            if test_case_name is None:
                test_case_name = pytest.current_test_name()

            # Wait for the element before taking the screenshot
            if locator:
                element = self.get_element(locator, timeout=timeout, polling=polling)
                locator_info = f" (Locator: {locator})"
            else:
                element = None
                locator_info = ""

            # Create file name with timestamp
            file_name = f"{test_case_name}.{int(time.time() * 1000)}.png"
            screenshot_directory = "../screenshots/"
            relative_filename = os.path.join(screenshot_directory, file_name)
            current_directory = os.path.dirname(__file__)
            destination_file = os.path.join(current_directory, relative_filename)
            destination_directory = os.path.join(current_directory, screenshot_directory)

            # Save screenshot
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)

            if element:
                element.screenshot(destination_file)
            else:
                self.driver.save_screenshot(destination_file)

            self.logger.info(f"Screenshot saved to directory: {destination_file}{locator_info}")
        except FileNotFoundError as fnf_error:
            self.logger.error("### Error occurred when taking screenshot: File not found.")
            self.logger.error(fnf_error)
        except PermissionError as perm_error:
            self.logger.error("### Error occurred when taking screenshot: Permission denied.")
            self.logger.error(perm_error)
        except Exception as e:
            self.logger.error("### Exception occurred when taking screenshot")
            self.logger.error(e)

    def select_from_drop_down(self, select_value, locator, locator_type="id", select_by='index', timeout=10,
                              polling=0.5):
        """
        Selects an option from a drop-down menu.

        Args:
            select_value: The value, index, or visible text of the option to select.
            locator: The locator tuple (strategy, value) used to find the drop-down element.
            locator_type: The type of locator to be used (default is "id").
            select_by: The method to use for selecting the option ('val' for value, 'index' for index, 'text' for visible text).
            timeout: Maximum time to wait for the drop-down element to be found (default is 10 seconds).
            polling: The sleep interval between retries (default is 0.5 seconds).
        """
        try:
            element = self.get_element(locator, timeout=timeout, polling=polling, multiple=False)
            sel = Select(element)

            select_methods = {
                'val': sel.select_by_value,
                'index': lambda value: sel.select_by_index(int(value)),
                'text': sel.select_by_visible_text,
            }

            select_by = select_by.lower()
            if select_by in select_methods:
                select_methods[select_by](select_value)
                self.logger.info(f"Selected option '{select_value}' from drop-down using '{select_by}' method.")
            else:
                self.logger.error(f"Cannot select with the given 'select_by' method: {select_by}")
        except NoSuchElementException:
            self.logger.error(f"Drop-down element not found with locator: {locator}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")

    def do_alt_click(self, locator, params=None, timeout=None):
        """
        Alt-click web element.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            params: Additional parameters for locating the element (optional).
            timeout: Maximum time to wait for the element to be found (optional).
        """
        try:
            element = self.get_element(locator, timeout=timeout)
            action_chain = ActionChains(self.driver)
            action_chain.key_down(Keys.ALT).click(element).key_up(Keys.ALT).perform()
            self.logger.info(f"Alt-clicked element with locator: {locator}")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def do_shift_click(self, locator, params=None, timeout=None):
        """
        Shift-click web element.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            params: Additional parameters for locating the element (optional).
            timeout: Maximum time to wait for the element to be found (optional).
        """
        try:
            element = self.get_element(locator, timeout=timeout)
            action_chain = ActionChains(self.driver)
            action_chain.key_down(Keys.SHIFT).click(element).key_up(Keys.SHIFT).perform()
            self.logger.info(f"Shift-clicked element with locator: {locator}")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def do_multi_click(self, locator, params=None, timeout=None):
        """
        Presses left control or command button depending on OS, clicks and then releases control or command key.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            params: Additional parameters for locating the element (optional).
            timeout: Maximum time to wait for the element to be found (optional).
        """
        try:
            element = self.get_element(locator, timeout=timeout)
            action_chain = ActionChains(self.driver)
            action_chain.key_down(Keys.LEFT_CONTROL if sys.platform == 'win32' else Keys.COMMAND).click(element).key_up(
                Keys.LEFT_CONTROL if sys.platform == 'win32' else Keys.COMMAND).perform()
            self.logger.info(f"Multi-clicked element with locator: {locator}")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def do_shift_select(self, first_element, last_element):
        """
        Shift-select web elements.

        Args:
            first_element: The locator tuple (strategy, value) of the first element to click.
            last_element: The locator tuple (strategy, value) of the last element to shift-click.
        """
        try:
            first = self.get_element(first_element)
            last = self.get_element(last_element)
            action_chain = ActionChains(self.driver)
            action_chain.click(first).key_down(Keys.SHIFT).click(last).key_up(Keys.SHIFT).perform()
            self.logger.info(f"Shift-selected elements from {first_element} to {last_element}")
        except NoSuchElementException:
            self.logger.error(f"One of the elements not found: {first_element}, {last_element}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def do_multi_select(self, elements_to_select):
        """
        Multi-select any number of elements.

        Args:
            elements_to_select: A list of locator tuples (strategy, value) of elements to select.
        """
        try:
            action_chain = ActionChains(self.driver)
            for element_locator in elements_to_select:
                element = self.get_element(element_locator)
                action_chain.key_down(Keys.LEFT_CONTROL if sys.platform == 'win32' else Keys.COMMAND).click(element)
            action_chain.key_up(Keys.LEFT_CONTROL if sys.platform == 'win32' else Keys.COMMAND).perform()
            self.logger.info(f"Multi-selected elements: {elements_to_select}")
        except NoSuchElementException:
            self.logger.error(f"One of the elements not found: {elements_to_select}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def move_to_element(self, locator, params=None, timeout=None):
        """
        Move to web element.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            params: Additional parameters for locating the element (optional).
            timeout: Maximum time to wait for the element to be found (optional).
        """
        try:
            element = self.get_element(locator, timeout=timeout)
            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(element).perform()
            self.logger.info(f"Moved to element with locator: {locator}")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def get_attribute(self, locator, attribute, params=None, timeout=None, visible=False):
        """
        Get attribute from element based on locator with optional parameters.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            attribute: The attribute to retrieve from the element.
            params: Additional parameters for locating the element (optional).
            timeout: Maximum time to wait for the element to be found (optional).
            visible: Flag indicating whether the element should be visible (optional).
        """
        try:
            element = self.get_element(locator, timeout=timeout, visible=visible)
            attr_value = element.get_attribute(attribute)
            self.logger.info(f"Attribute '{attribute}' value for element with locator {locator}: {attr_value}")
            return attr_value
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def drag_and_drop(self, source_element, target_element, params=None):
        """
        Drag source element and drop at target element.

        Args:
            source_element: The locator tuple (strategy, value) of the source element to drag.
            target_element: The locator tuple (strategy, value) of the target element to drop onto.
            params: Additional parameters for locating the elements (optional).
        """
        try:
            source = self.get_element(source_element)
            target = self.get_element(target_element)
            action_chain = ActionChains(self.driver)
            action_chain.drag_and_drop(source, target).perform()
            self.logger.info(f"Dragged element from {source_element} to {target_element}")
        except NoSuchElementException:
            self.logger.error(f"One of the elements not found: {source_element}, {target_element}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def is_element_with_text_present(self, locator, text, params=None, visible=False, exact_match=False):
        """
        Check if element with specified text is present.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            text: The text to search for within the element.
            params: Additional parameters for locating the element (optional).
            visible: Flag indicating whether the element should be visible (optional).
            exact_match: Flag indicating whether to perform an exact match on the text (optional).

        Returns:
            bool: True if element with specified text is present, False otherwise.
        """
        try:
            element = self.get_element(locator, visible=visible)
            element_text = element.text if exact_match else element.get_attribute("innerHTML")
            if text in element_text:
                self.logger.info(f"Element with text '{text}' found at locator: {locator}")
                return True
            else:
                self.logger.info(f"Element with text '{text}' not found at locator: {locator}")
                return False
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            return False
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return False

    def scroll_element_into_view(self, locator):
        """
        Scrolls an element into view.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
        """
        try:
            element = self.get_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f"Scrolled element with locator {locator} into view")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def open_hover(self, locator, params=None, use_js=False):
        """
        Open a hover or popover.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            params: Additional parameters for locating the element (optional).
            use_js: Flag indicating whether to use JavaScript to trigger the hover action (optional).
        """
        try:
            element = self.get_element(locator)
            if use_js:
                self.driver.execute_script(
                    "arguments[0].dispatchEvent(new MouseEvent('mouseover', { 'bubbles': true, 'cancelable': true }))",
                    element)
            else:
                action_chain = ActionChains(self.driver)
                action_chain.move_to_element(element).perform()
            self.logger.info(f"Hovered over element with locator: {locator}")
        except NoSuchElementException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def perform_hover_action(self, locator, func, error_msg='', exceptions=None, params=None,
                             alt_loc=None, alt_params=None, **kwargs):
        """
        Hovers an element and performs whatever action is specified in the supplied function.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element to hover over.
            func: The function to perform after hovering over the element.
            error_msg: Error message to log if the hover action fails (optional).
            exceptions: Exceptions to catch and handle (optional).
            params: Additional parameters for locating the element to hover over (optional).
            alt_loc: Alternative locator to use if the first locator is not found (optional).
            alt_params: Additional parameters for locating the alternative element (optional).
            **kwargs: Additional keyword arguments to pass to the function.
        """
        try:
            element = self.get_element(locator, params=params)
            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(element).perform()
            self.logger.info(f"Hovered over element with locator: {locator}")
            func(**kwargs)
        except NoSuchElementException:
            if alt_loc:
                alt_element = self.get_element(alt_loc, params=alt_params)
                action_chain = ActionChains(self.driver)
                action_chain.move_to_element(alt_element).perform()
                self.logger.info(f"Hovered over alternative element with locator: {alt_loc}")
                func(**kwargs)
            else:
                self.logger.error(f"Element not found with locator: {locator}")
                raise
        except exceptions as e:
            self.logger.error(f"{error_msg}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def wait_for_element_to_disappear(self, locator, params=None, timeout=None):
        """
        Waits until the element is not visible (hidden) or no longer attached to the DOM.

        Args:
            locator: The locator tuple (strategy, value) used to find the web element.
            params: Additional parameters for locating the element (optional).
            timeout: Maximum time to wait for the element to disappear (optional).
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout)
            wait.until_not(EC.visibility_of_element_located(locator))
            self.logger.info(f"Element with locator {locator} has disappeared")
        except TimeoutException:
            self.logger.error(f"Element with locator {locator} did not disappear within the specified timeout")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def wait_for_ajax_calls_to_complete(self, timeout=5):
        """
        Waits until there are no active or pending ajax requests.

        Args:
            timeout: Maximum time to wait for ajax calls to complete (optional).
        """
        try:
            wait = WebDriverWait(self.driver, timeout=timeout)
            wait.until(lambda driver: self.driver.execute_script("return jQuery.active == 0"))
            self.logger.info("All AJAX calls have completed")
        except TimeoutException:
            self.logger.error("Timed out waiting for AJAX calls to complete")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise
