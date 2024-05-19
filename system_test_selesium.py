#system test

import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        edge_service = EdgeService(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=edge_service)
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        self.driver.quit()

    def test_register_login_and_access(self):
        driver = self.driver

        # Register a new user
        driver.find_element(By.LINK_TEXT, 'Register').click()
        driver.find_element(By.NAME, 'username').send_keys('testuser')
        driver.find_element(By.NAME, 'email').send_keys('test@example.com')
        driver.find_element(By.NAME, 'password').send_keys('testpassword')
        driver.find_element(By.NAME, 'password2').send_keys('testpassword')
        driver.find_element(By.NAME, 'submit').click()
        
        # Wait until the registration is complete
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.alert'))
        )

        # Check if registration was successful
        alert_text = driver.find_element(By.CSS_SELECTOR, 'div.alert').text
        self.assertIn('Congratulations, you are now a registered user!', alert_text)

        # Login with the newly registered user
        driver.find_element(By.LINK_TEXT, 'Login').click()
        driver.find_element(By.NAME, 'username').send_keys('testuser')
        driver.find_element(By.NAME, 'password').send_keys('testpassword')
        driver.find_element(By.NAME, 'submit').click()

        # Wait until login is complete
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Profile'))
        )

        # Check if login was successful
        self.assertIn('Home', driver.page_source)

        # Access a protected page
        driver.find_element(By.LINK_TEXT, 'Home').click()

        # Wait for the protected page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        # Check if the protected page loaded correctly
        self.assertIn('Home', driver.page_source)

if __name__ == '__main__':
    unittest.main()
