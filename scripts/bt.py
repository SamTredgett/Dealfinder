"""
    Dealfinder is a webscraping script designed to search broadband sites for deals given a postcode available and then
    manipulate this information for the user.

    This script uses the Chrome webdriver to target objects on the site https://www.bt.com/products/broadband/broadband-learn
    and query it for deals against a certain post-code.
    Author: Sam Tredgett
    Date of Creation: 17/11/2021
    Last updated: 18/11/2021

"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from pathlib import Path
import pandas as pd
import os

# Sets up the web driver
os.environ['PATH']

postcode = "cm27qh"
house_number = "30"
with webdriver.Chrome() as driver:
    # Load site
    driver.get('https://www.bt.com/products/broadband/deals')

    # Get rid of cookies dialog box
    driver.switch_to.frame(0)
    driver.find_element(By.CLASS_NAME, "call").click()
    driver.switch_to.default_content()

    # Grab input field
    search = driver.find_element(By.ID, "sc-postcode")

    print(type(search))
    print(search)
    # Put our information into it and hit enter
    query = postcode
    search.send_keys(query + Keys.RETURN)

    # Wait for it to load the dropdown
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tvsc-address"))
    )
    dropdown = driver.find_element(By.ID, "tvsc-address")
    print('page loaded')
    #  Select the dropdown box

    select = Select(dropdown)
    # Try to select our house number from the drop-down
    try:
        select.select_by_index(1)
        dropdown_found = True
    except NoSuchElementException:
        print("Not found! Please make sure you've input a correct house number and postcode")

    #  Grab the confirm button that appears and click it
    if dropdown_found:
        button = driver.find_element(By.ID, "btnCustomConfirmAddress")
        button.click()

    # Now select the results
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'product-list'))
    )

    products = driver.find_elements(By.ID, 'product-list')
    for product in products:
        # Grab lists of each element we need to return
        names = driver.find_elements(By.ID, "product-name")
        speeds = driver.find_elements(By.CLASS_NAME, 'jss906')
        costs = driver.find_elements(By.ID, "product-price")
        contracts = driver.find_elements(By.ID, "contract-length")
        upfronts = driver.find_elements(By.ID, "upfront-section")

        print(names)
        print(speeds)
        print(costs)
        print(upfronts)

    for name in names:
        print(name.text)
    time.sleep(2000)
    print("finished running")
