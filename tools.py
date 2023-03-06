from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
import time

PROQUEST_URL = "http://search.proquest.com.ezp-prod1.hul.harvard.edu/news/advanced?accountid=11311"

def init_webdriver():
    options = Options()
    # options.headless = True 
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options = options)
    driver.set_page_load_timeout(60)
    return driver

def login_proquest(driver):
    driver.get(PROQUEST_URL)

    # Log in to my.harvard
    username = os.environ.get("harvard_username")
    password = os.environ.get("harvard_password")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "submit").click()

    # Wait for Duo Authentication to be completed
    time.sleep(15)

    # Trust Browser
    driver.find_element(By.ID, "trust-browser-button").click()
    time.sleep(15)
    

    



