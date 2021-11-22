"""
    Dealfinder is a webscraping script designed to search broadband sites for deals given a postcode available and then
    manipulate this information for the user.

    This script uses the Chrome webdriver to target objects on the site https://www.bt.com/products/broadband/broadband-learn
    and query it for deals against a certain post-code.
    Author: Sam Tredgett
    Date of Creation: 17/11/2021
    Last updated: 19/11/2021

"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchFrameException
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
    time.sleep(10)
    # There is some inconsistencies with how this runs, unsure why as of now, using WebDriverWait didn't fix
    driver.switch_to.frame(1)
    driver.find_element(By.CLASS_NAME, "call").click()
    driver.switch_to.default_content()

    # Grab input field
    search = driver.find_element(By.ID, "sc-postcode")

    # Input postcode and search
    search.send_keys(postcode + Keys.RETURN)

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
    # Catch the failed attempt for bad postcodes
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

    # Iterate over returned results and pack them into lists of web elements

    first = True

    for product in products:
        # Grab lists of each element we need to return
        names = driver.find_elements(By.ID, "product-name")
        speeds = driver.find_elements(By.CLASS_NAME, 'jss904')
        costs = driver.find_elements(By.ID, "product-price")
        contracts = driver.find_elements(By.ID, "contract-length")
        upfronts = driver.find_elements(By.ID, "upfront-section")

    # Need to add the first product card to front as it's labelled weirdly in their HTML
    speeds.insert(0, driver.find_element(By.CLASS_NAME, 'jss903'))

    # Change the data from a web element to a string in each list
    for num in range(0, len(names)):
        names[num] = names[num].text
        speeds[num] = speeds[num].text
        costs[num] = costs[num].text
        contracts[num] = contracts[num].text
        upfronts[num] = upfronts[num].text

    data = {'name': names, 'speed': speeds, 'cost': costs, 'contract': contracts, 'upfront': upfronts}
    df = pd.DataFrame(data)
    print(df)
    # Save to CSV file
    file_name = input("Please enter the name you'd like to call the CSV file of your output: ")
    df.to_csv(f'{file_name}_.csv')

    print("finished running")
