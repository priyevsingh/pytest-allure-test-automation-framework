import allure
from Base.base import BaseClass
from Pages.HomePage import HomePage


class TestHomePage(BaseClass):

    """
    This class contains all the test methods for HomePage, and inherits from BaseClass.
    """

    @allure.issue("<feature-issue-number-and-details>")
    @allure.description("Test To Verify Home Page Button")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.epic("Home Page Features")
    @allure.testcase(
        "<url-link-to-your-work-item-manual-test-case>", "<your-test-case-description>"
    )
    def test_google_feeling_lucky_feature(self):
        try:
            home = HomePage(self.logger, self.driver, self.wait)
            home.google_feeling_lucky_feature()

        except Exception as e:
            self.logger.error("Error at ", exc_info=True)
        finally:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
