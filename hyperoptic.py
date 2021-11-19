"""
    Dealfinder is a webscraping script designed to search broadband sites for deals given a postcode available and then
    manipulate this information for the user.

    This script uses the Chrome webdriver to target objects on the site https://www.hyperoptic.com/ and query it for deals
    against a certain post-code.
    Author: Sam Tredgett
    Date of Creation: 17/11/2021
    Last updated: 18/11/2021

"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from pathlib import Path
import pandas as pd
import os

# Sets up the web driver
os.environ['PATH']

# Test postcode here was one of the few I managed to find that actually returned a result available to be processed
postcode = "SW1V 1AG"

with webdriver.Chrome() as driver:
    # Load site
    driver.get('https://www.hyperoptic.com/')

    # Grab input field
    search = driver.find_element(By.XPATH, '//*[@id="block_5d417545412ba"]/div/div[1]/div/div/div[1]/div/div/input')

    #  Go away cookie notification
    cookies = driver.find_element(By.CLASS_NAME, "modal-button")
    cookies.click()

    # Select the search bar, pass in postcode and generate the dropdown
    search.click()
    search.send_keys(postcode + Keys.RETURN)

    # Wait for dropdown and select it
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "elastic-results-container"))
    )
    dropdown = driver.find_element(By.CLASS_NAME, "elastic-results-container")
    print('page loaded')

    # Wait until dropdown loads
    dropdown_wait = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="elastic-results"]/div[2]/div[1]'))
    )
    # Select dropdown element
    dropdown_item = driver.find_element(By.XPATH, '//*[@id="elastic-results"]/div[2]/div[1]')
    dropdown_item.click()
    print('dropdown item selected')
    # Wait for button to be clickable
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="block_5d417545412ba"]/div/div[1]/div/div/div[1]/div/div/button'))
    )
    search_button = driver.find_element(By.XPATH,
                                        '//*[@id="block_5d417545412ba"]/div/div[1]/div/div/div[1]/div/div/button')
    search_button.click()

    # Selecting the content blocks for each price structure
    parent_node = WebDriverWait(driver, 10).until(
                            lambda br: br.find_elements(By.CLASS_NAME, 'package-col'))
    print(parent_node[0])

    # Get the child elements from this
    children = parent_node[0].find_elements(By.XPATH, './*')

    # Set up base list
    names = ["fast", "superfast", "ultrafast", "hyperfast"]
    # Iterate over child nodes to pull out data
    for child in children:
        speeds = driver.find_elements(By.CLASS_NAME, "size-unit")
        costs = driver.find_elements(By.CLASS_NAME, "price")
        contracts = driver.find_elements(By.CLASS_NAME, "promotion-months")
        upfronts_web = driver.find_elements(By.CLASS_NAME, "description")

    '''
        loop over the length of all the lists and sanitise data in various ways
        string formatting for the upfront costs
        converting web objects into strings for others
    '''
    upfronts = []
    for num in range(0, len(names)):
        sanitised_num = f"£{upfronts_web[num].text.split('£')[1].split('and')[0]}"
        upfronts.insert(num, sanitised_num)
        speeds[num] = speeds[num].text
        costs[num] = costs[num].text
        contracts[num] = contracts[num].text

    # Package data into a dictionary ready to convert to a dataframe
    data = {
        'name': names,
        'speed': speeds,
        'monthly_cost': costs,
        'contract_length': contracts,
        'upfront': upfronts}
    df = pd.DataFrame(data)
    print(df)

    # Query user for a desired filename and save information to userinput_.csv
    file_name = input("Please enter the name you'd like to call the CSV file of your output: ")
    df.to_csv(f'{file_name}_.csv')

