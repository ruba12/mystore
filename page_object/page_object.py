"""Page object creates an object repository for storing all web elements. It is useful in reducing code duplication and
improves test case maintenance"""
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from base import URLS, PageObject


class Object(PageObject):
    url = URLS['my_store']
    username_locator = By.ID, 'email_create'
    password_locator = By.ID, 'id_password'
    submit_button_locator = By.CSS_SELECTOR, ".btn.btn-default.button.button-medium.exclusive"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = self.get_random_chars().capitalize()
        self.last_name = "Test"
        self.phone_number = self.get_random_phone_number()
        self.new_email = f"{self.first_name}@Test.com"
        self.full_name = f"{self.first_name} Test"
        self.postcode = "12343"
        self.address = "8th Avenue Street"
        self.city = "Hokaido"
        self.company = "Fave"

    """ Validate if user can register a valid email"""
    def login_as_user(self):
        # navigate to url
        self.driver.get(self.url)
        # navigate to sign up page
        self.driver.find_element(By.CSS_SELECTOR, "a.login").click()
        self.short_wait()
        username_input = self.wait.until(ec.visibility_of_element_located(self.username_locator))
        submit_button = self.wait.until(ec.element_to_be_clickable(self.submit_button_locator))
        # enter your valid email address
        email_flag = False
        while not email_flag:
            email = self.new_email
            # validate user email
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):  # if the email is valid
                email_flag = True
                # username
                username_input.send_keys(self.new_email)
                self.long_wait()
                # login button
                submit_button.click()
                self.long_wait()
            else:  # the email is invalid
                username_input.send_keys(self.new_email)
                self.long_wait()
                # login button
                submit_button.click()
                self.long_wait()
                assert self.driver.find_element(
                    By.CSS_SELECTOR, "#create_account_error > ol > li").text == "Invalid email address."
                break
                # allow email_flag to remain false

    """ Validate if user can create account"""
    def create_account(self):
        # select title
        self.driver.find_element_by_css_selector("input[id='id_gender2']").click()
        self.short_wait()
        # enter first name
        self.driver.find_element(By.ID, "customer_firstname").send_keys(self.first_name)
        self.short_wait()
        # enter last name
        self.driver.find_element(By.ID, "customer_lastname").send_keys(self.last_name)
        self.short_wait()
        # enter password
        self.driver.find_element(By.ID, "passwd").send_keys(self.password_generator())
        self.short_wait()
        # enter dob
        # select day
        day = Select(self.driver.find_element(By.ID, "days"))
        day.select_by_index(2)
        # select month
        day = Select(self.driver.find_element(By.ID, "months"))
        day.select_by_index(2)
        # select year
        day = Select(self.driver.find_element(By.ID, "years"))
        day.select_by_index(2)
        # YOUR ADDRESS
        # enter company
        self.driver.find_element(By.ID, "company").send_keys(self.company)
        self.short_wait()
        # enter address1
        self.driver.find_element(By.ID, "address1").send_keys(self.address)
        self.short_wait()
        # enter city
        self.driver.find_element(By.ID, "city").send_keys(self.city)
        self.short_wait()
        # enter state
        state = Select(self.driver.find_element(By.ID, "id_state"))
        state.select_by_index(2)
        self.short_wait()
        self.short_wait()
        # enter postcode
        self.driver.find_element(By.ID, "postcode").send_keys(self.postcode)
        self.short_wait()
        # enter country
        country = Select(self.driver.find_element(By.ID, "id_country"))
        country.select_by_index(1)
        self.short_wait()
        # enter phone mobile
        self.driver.find_element(By.ID, "phone_mobile").send_keys(self.phone_number)
        self.short_wait()
        # enter submit button
        self.driver.find_element(By.CSS_SELECTOR, "#submitAccount > span").click()
        return country

    """Validate is a user able to add items to cart"""
    def add_to_cart(self):
        # click Home button
        self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[3]/div/ul/li/a/span").click()
        self.long_wait()
        # scroll page down
        self.driver.execute_script("window.scrollTo(0, 700)")
        self.long_wait()
        # hover over the element
        element = self.driver.find_element(
            By.CSS_SELECTOR, "#homefeatured > li:nth-child(2)")
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()
        self.short_wait()
        product_name = self.driver.find_element(
            By.CSS_SELECTOR,
            "#homefeatured > li.ajax_block_product.col-xs-12.col-sm-4.col-md-3"
            ".last-item-of-mobile-line.hovered h5 > a").text
        self.short_wait()
        #  add item to cart
        self.driver.find_element(
            By.CSS_SELECTOR,
            "#homefeatured > li:nth-child(2) > div > div.right-block > div.button-container"
            " > a.button.ajax_add_to_cart_button.btn.btn-default > span").click()
        self.short_wait()
        message = self.driver.find_element(
            By.XPATH, "/html/body/div/div[1]/header/div[3]/div/div/div[4]/div[1]/div[1]/h2").text
        message.strip()
        self.short_wait()
        quantity = self.driver.find_element(
            By.XPATH, "/html/body/div/div[1]/header/div[3]/div/div/div[4]/div[1]/div[1]/div[2]/div[1]/span").text
        self.long_wait()
        unit_price = self.driver.find_element(By.CSS_SELECTOR, "span#layer_cart_product_price").text[1:]
        self.short_wait()
        total_price = int(quantity) * int(float(unit_price))
        self.short_wait()
        # verify the quantity with unit price to get the total price
        state_price = self.driver.find_element(By.CSS_SELECTOR, "span.ajax_block_products_total").text[1:3]
        state_price = int(state_price)
        self.short_wait()
        assert total_price == state_price
        self.short_wait()
        # Verify the product
        assert self.driver.find_element(
            By.XPATH,
            "/html/body/div/div[1]/header/div[3]/div/div/div[4]/div[1]/div[1]/div[2]/span[1]").text == product_name
        self.short_wait()
        # continue shopping
        self.driver.find_element(By.CSS_SELECTOR, ".continue.btn.btn-default.button.exclusive-medium").click()
        self.short_wait()
        element = self.driver.find_element(
            By.CSS_SELECTOR, "#homefeatured > li:nth-child(4)")
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()
        self.short_wait()
        # add another product
        self.driver.find_element(
            By.XPATH,
            "/html/body/div/div[2]/div/div[2]/div/div[1]/ul[1]/li[4]/div/div[2]/div[2]/a[1]").click()
        # proceed to checkout
        self.driver.find_element(By.CSS_SELECTOR, "div.layer_cart_cart.col-xs-12.col-md-6  a > span").click()

    """Validate if user can make purchase/payment"""

    def make_purchase(self):
        total_product = self.driver.find_element(By.ID, "total_product").text[1:]
        total_shipping = self.driver.find_element(By.ID, "total_shipping").text[1:]
        total_product_shipping = int(float(total_product)) + int(float(total_shipping))
        tax = self.driver.find_element(By.ID, "total_tax").text[1:]
        total_price_with_tax = total_product_shipping + int(float(tax))
        total_price = self.driver.find_element(By.ID, "total_price").text[1:3]
        total_price = int(total_price)
        assert total_price_with_tax == total_price
        # proceed to checkout
        self.driver.find_element(
            By.CSS_SELECTOR, "a.button.btn.btn-default.standard-checkout.button-medium > span").click()
        self.short_wait()
        self.driver.find_element(
            By.CSS_SELECTOR, "button.button.btn.btn-default.button-medium").click()
        # get the delivery/shipping price
        delivery_price = self.driver.find_element(By.CSS_SELECTOR, "td.delivery_option_price > div").text[1:]
        self.short_wait()
        # click on the checkbox
        self.driver.find_element(By.ID, "cgv").click()
        self.short_wait()
        # click the proceed to checkout button
        self.driver.find_element(
            By.CSS_SELECTOR, "button.button.btn.btn-default.standard-checkout.button-medium").click()
        # payment by bank wire
        self.driver.find_element(By.CSS_SELECTOR, "#HOOK_PAYMENT div:nth-child(1) a").click()
        # click confirm order
        self.driver.find_element(By.CSS_SELECTOR, "#cart_navigation > button > span").click()

    """Validate if user can view order details/history and download the invoice pdf"""
    def order_details(self):
        # click on account name
        self.driver.find_element(By.CSS_SELECTOR, "a.account").click()
        self.short_wait()
        # click on order and history details
        self.driver.find_element(By.CSS_SELECTOR, "#center_column a > span").click()
        # click on the reference number
        self.driver.find_element(By.CSS_SELECTOR, "a.color-myaccount").click()
        # scroll page down
        self.driver.execute_script("window.scrollTo(0, 450)")
        self.long_wait()
        # TODO: download pdf
        # click on pdf
        pdf = self.driver.find_element(
            By.CSS_SELECTOR, "#order-list > tbody > tr > td.history_invoice > a").get_attribute('href')
        self.short_wait()
        # download the pdf
        self.driver.get(pdf)
        self.long_wait()
        # sign out from the website
        self.driver.find_element(By.CSS_SELECTOR, "a.logout").click()
