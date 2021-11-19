"""
    Dealfinder is a webscraping script designed to search broadband sites for deals given a postcode available and then
    manipulate this information for the user.
    Author: Sam Tredgett
    Date of Creation: 17/11/2021
    Last updated: 18/11/2021

"""
import os
from selenium import webdriver


os.environ['PATH']
driver = webdriver.Chrome()
driver.get()