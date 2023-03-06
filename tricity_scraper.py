from bs4 import BeautifulSoup
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from tools import init_webdriver, login_proquest
import time


# Proquest Tri-City Herald url 
URL = "https://www.proquest.com/usnews/publication/45003"

# CSV file to save scraped data
csv_file = "scraped_data.csv"


# Chromedriver instance 
driver = init_webdriver()


def open_url():
    driver.get(URL)
    time.sleep(10)


def set_date_parameters(month, date=None):
    select = Select(driver.find_element(By.ID, "yearSelected"))
    select.select_by_value("2011")
    time.sleep(2)
    select = Select(driver.find_element(By.NAME, "monthSelected"))
    select.select_by_value(month)
    time.sleep(2)
    select = Select(driver.find_element(By.NAME, "issueSelected"))
    if not date:
        select.select_by_index(len(select.options) - 1)
    else:
        select.select_by_visible_text(date)
    time.sleep(1)
    driver.find_element(By.NAME, "searchPubIssues").click()
    time.sleep(5)
    

def start_search(writer):
    end_date = driver.find_element(By.ID, "IssueDetails").text
    while "Jan 1, 2012" not in end_date:
        find_birth_entries(writer)
        li = driver.find_element(By.CSS_SELECTOR, ".pull-right.nextLink")
        li.find_element(By.TAG_NAME, "a").click()
        try:
            time.sleep(5)
            end_date = driver.find_element(By.ID, "IssueDetails").text
        except:
            print("here")
            time.sleep(5)
            end_date = driver.find_element(By.ID, "IssueDetails").text
    return 


def find_birth_entries(writer):
    for entry in driver.find_elements(By.CLASS_NAME, "resultHeader"):
        title = entry.find_element(By.CLASS_NAME, "truncatedResultsTitle").text
        if "Births" in title:
            link = entry.find_element(By.TAG_NAME, "a")
            births = parse_newslink(link)
            writer.writerow(births)
            print(title)
            print(births)
    return
            

def parse_newslink(link):
    # Open link in new tab
    main_window = driver.current_window_handle
    link.send_keys(Keys.CONTROL + Keys.SHIFT + Keys.RETURN)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    # Extract text 
    births = []
    content = driver.find_element(By.CLASS_NAME, "abstractContainer")
    for entry in content.find_elements(By.TAG_NAME, "p"):
        text = entry.text.lstrip().rstrip()
        if text:
            births.append(text)

    # Close tab
    driver.close()
    driver.switch_to.window(main_window)
    return births


def main():

    # Open CSV file
    file = open(csv_file, 'a')
    writer = csv.writer(file, delimiter=';')

    # Start scraping
    login_proquest(driver)
    open_url()
    set_date_parameters("08", "Aug 14, 2011")
    start_search(writer)

if __name__ == "__main__":
    main()