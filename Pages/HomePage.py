import pytest
import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotVisibleException,
    ElementNotSelectableException,
    InvalidElementStateException,
    WebDriverException,
    UnexpectedAlertPresentException,
)
from Resources.HomePageLocators import HomePageLocators


class HomePage:
    """
    Class for all Home Page related methods.
    """

    def __init__(self, logger, driver, wait):
        """
        Constructor for HomePage class.
        """
        self.logger = logger
        self.driver = driver
        self.wait = wait

    # all your other homepage features test functions will go here.

    @allure.step("<your-test-function-step-name>")
    @allure.feature("<your-test-function-feature-name>")
    def google_feeling_lucky_feature(self):
        """
        Click on I'm Feeling Lucky button
        :return:
        """
        try:
            ele = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, HomePageLocators.feeling_lucky_search_button_xpath)
                )
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)
            ele.click()
        except (
            NoSuchElementException,
            TimeoutException,
            StaleElementReferenceException,
        ) as e:
            self.logger.error(f"Error {e}", exc_info=True)
            pytest.fail(reason="Button was not found")
