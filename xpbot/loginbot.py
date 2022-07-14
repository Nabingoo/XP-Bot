from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
# Github credentials
usernameStr = "bradw"
passwordStr = "Bryan6411!"

"""
browser = webdriver.Chrome("chromedriver")
browser.get(('https://github.com/login'))
"""
"""
chromedriver = 'Macintosh HD/Users/navin/Desktop/loginbot/chromedriver'
browser = webdriver.Chrome(chromedriver)
browser.get(('https://github.com/login'))
"""
def loginmoment():

    threading.Timer(86400.0, loginmoment).start()

    usernameStr = "bradw"
    passwordStr = "Bryan6411!"
    chromedriver = '/Users/navin/Desktop/loginbot/chromedriver'
    browser = webdriver.Chrome(chromedriver)
    browser.get(('https://www.myedio.com/login/'))

    username = browser.find_element_by_id('username')
    username.send_keys(usernameStr)
    """
    password = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'Passwd')))
    password.send_keys(passwordStr)
    """
    password = browser.find_element_by_id('password')
    password.send_keys(passwordStr)

    #locator = "//c-button[span[text()='Log In']]"

    commitbutton = browser.find_element_by_class_name("c-button")
    commitbutton.click()

    time.sleep(10)

    browser.close()

loginmoment()