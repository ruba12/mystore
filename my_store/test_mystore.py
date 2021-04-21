"""
The test script consist of 4 scenarios which is:
1.Validate if a user can successfully register  and create an account with a valid username and password.
2.Validate that the user can buy products added to the cart after signing in to the application
(or as per the functionality of the website).
3.Validate if the user can add more than one product in the cart
4. Validate order delivery details and history
"""
from selenium.webdriver.common.by import By

from base import MyStore
from page_object.page_object import Object


class TestLoginPage(MyStore):
    result = None
    total_price_with_tax = None

    # validate login email
    def test_login(self):
        Object(self.driver).login_as_user()

    # verify if a user successfully created account
    def test_create_account(self):
        Object(self.driver).create_account()

    # verify it a user successfully added product to cart
    def test_add_to_cart(self):
        TestLoginPage.result = Object(self.driver).add_to_cart()
        number_of_items = self.driver.find_element(
            By.CSS_SELECTOR, "#center_column > h1 > span.heading-counter").text[:2]
        # validate the number of item in the page with result
        assert int(number_of_items) == TestLoginPage.result

    # verify if a user successfully make purchase
    def test_make_purchase(self):
        TestLoginPage.total_price_with_tax = Object(self.driver).make_purchase()
        total_price = self.driver.find_element(By.ID, "total_price").text[1:3]
        total_price = int(total_price)
        # verifying and asserting the total price with obtained total price with tax
        assert total_price == TestLoginPage.total_price_with_tax

    # verify if a user successfully make payment
    def test_checkout(self):
        Object(self.driver).checkout()

    # verify order details and history
    def test_order_details(self):
        Object(self.driver).order_details()
