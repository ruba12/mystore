"""
Base.py file contains functions which can be used globally for different types of project
"""
import os
import random
import string
import time
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


URLS = {
    'my_store': 'http://automationpractice.com/index.php'
}


class _TestCaseUtils(object):
    """General utility methods for writing test cases."""
    driver = None  # Chrome web driver
    url = None  # UAT domain name
    max_timeout = 60

    @staticmethod
    def get_random_chars():
        """Return random characters with random length of 7 to 10.
        :return: Random characters.
        """
        letters = list(string.ascii_lowercase)
        size = random.randint(7, 10)
        random.shuffle(letters)
        return ''.join(letters[:size])

    @staticmethod
    def short_wait():
        """Wait for 1 second."""
        time.sleep(1)

    @classmethod
    def get_random_email(cls):
        """Return an email address consisting of random letters.
        :return: A randomized email address.
        """
        domain = random.choice(['com', 'org', 'co.uk', 'com.my'])
        return f'{cls.get_random_chars()}@{cls.get_random_chars()}.{domain}'

    @staticmethod
    def get_random_phone_number(prefix='+6'):
        """Return a phone number consisting of random numbers.
        :param prefix: Prefix to prepend, e.g. +1, or set to an empty
        string for no prefix.
        :return: A randomized phone number.
        """
        numbers = random.randint(10 ** 8, 10 ** 9)
        return f'{prefix}0{numbers}'

    @staticmethod
    def get_random_number():
        """Return a phone number consisting of random numbers.

        :param prefix: Prefix to prepend, e.g. +1, or set to an empty
        string for no prefix.
        :return: A randomized phone number.
        """
        numbers = random.randint(10 ** 8, 10 ** 9)
        return f'0{numbers}'

    @staticmethod
    def password_generator(size=10):
        password = random.choice(string.digits)
        password += random.choice(string.ascii_uppercase)
        password += random.choice(string.ascii_lowercase)
        password += random.choice(string.punctuation)

        for i in range(size):
            password += random.choice(string.ascii_letters)

        password_list = list(password)
        password = ''.join(password_list)
        return password


class PageObject(_TestCaseUtils):
    """Page Object model is an object design pattern, where web pages
    are represented as classes, and various elements on the page are
    defined as variables on the class. All possible user interactions
    can then be implemented as methods."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.max_timeout)


class _AbstractTestCase(_TestCaseUtils):
    """Abstract Selenium test case class that Selenium tests must
    inherit from.
    """

    @staticmethod
    def _get_driver_options():
        """Return options for Google Chrome WebDriver.
        :return: An instance of ChromeOptions() with additional
        arguments.
        """
        options = webdriver.ChromeOptions()
        # The env variable HEADLESS_CHROME can be set to true in order
        # to run Google Chrome in a headless mode.
        if os.getenv('HEADLESS_CHROME') is not None:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
        )
        return options

    @classmethod
    def setup_class(cls):
        # Set up Google Chrome WebDriver
        cls.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=cls._get_driver_options()
        )
        cls.driver.implicitly_wait(cls.max_timeout)
        cls.driver.set_window_position(0, 0)
        cls.wait = WebDriverWait(cls.driver, cls.max_timeout)

    @classmethod
    def teardown_class(cls):
        # If the env variable QUIT_CHROME_ON_TEARDOWN is set, then close
        # the browser upon tests completion.
        if os.getenv('QUIT_CHROME_ON_TEARDOWN') is not None:
            cls.driver.quit()


class MyStore(_AbstractTestCase):
    """Base test case for MyStore.
    All MyStore test cases must inherit from this class.
    """

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.url = URLS['my_store']
