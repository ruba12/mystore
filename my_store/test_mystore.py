"""
The test script consist of 4 scenarios which is:
1.Validate if a user can successfully register  and create an account with a valid username and password.
2.Validate that the user can buy products added to the cart after signing in to the application
(or as per the functionality of the website).
3.Validate if the user can add more than one product in the cart
4. Validate order delivery details and history
"""
from base import MyStore
from page_object.page_object import Object


class TestLoginPage(MyStore):

    # validate login email
    def test_login(self):
        Object(self.driver).login_as_user()
        self.short_wait()

    # verify if a user successfully created account
    def test_create_account(self):
        Object(self.driver).create_account()
        self.short_wait()

    # verify it a user successfully added product to cart
    def test_add_to_cart(self):
        Object(self.driver).add_to_cart()

    # verify if a user successfully make purchase
    def test_make_purchase(self):
        Object(self.driver).make_purchase()

    # verify order details and history
    def test_order_details(self):
        Object(self.driver).order_details()
        self.short_wait()
