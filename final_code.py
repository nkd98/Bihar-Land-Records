# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 10:57:22 2023

@author: Niruj
"""

### IMPORTS

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from selenium.webdriver.support.select import Select
import pandas as pd
import requests

from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By  


## 1. Go to the website: https://biharbhumi.bihar.gov.in/Biharbhumi/
# input url and intialize driver
url = 'https://biharbhumi.bihar.gov.in/Biharbhumi/'
 
driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install())) 
 
driver.get(url) 
 

# Increase the window size to find elements
driver.maximize_window()


## 2. Select “जमाबंदी पंजी देखें” to go to the next page
element = (driver.find_element(By.CSS_SELECTOR, "#playground > div.wrapper.d-flex > div > div > div > div > div.row.mbr-justify-content-center > div > div > div:nth-child(9) > a > div"))
element.click()

# Switch to the new tab
driver.switch_to.window(driver.window_handles[-1])

# Choose district
element = (driver.find_element(By.CSS_SELECTOR, "#MainContent_ddlDistrict > option:nth-child(2)"))
element.click()

# Allow some time to reload
import time
time.sleep(3)

# choose anchal
element = (driver.find_element(By.CSS_SELECTOR, "#MainContent_ddlCircle > option:nth-child(2)"))
element.click()

# click proceed
element = (driver.find_element("id", "MainContent_btnproceed"))
element.click()

time.sleep(1)
# select halka
element = (driver.find_element(By.CSS_SELECTOR, "#MainContent_ddlHalka > option:nth-child(2)"))
element.click()


# select mouza
time.sleep(2)
element = (driver.find_element(By.CSS_SELECTOR, "#MainContent_ddlMauja > option:nth-child(2)"))
element.click()

# select samasti 2 panji...
element = (driver.find_element("id", "MainContent_rdo_All"))
element.click()


time.sleep(4)

## Solve the captcha
# Read the numbers displayed
element = (driver.find_element(By.CSS_SELECTOR, "#MainContent_TextBox1"))

value = element.get_attribute("value")

# calculate captcha
captcha = eval(value)

# captcha input
element = (driver.find_element("id", "MainContent_TextBox2"))
element.click()
element.send_keys(captcha) # type the captcha

# click Submit 
element = (driver.find_element("id", "MainContent_btnSearch"))
element.click()

time.sleep(5)
# Show more recrods per page
element = (driver.find_element(By.CSS_SELECTOR, "#MainContent_ddl_view > option:nth-child(11)"))
element.click()

time.sleep(5)

## Pagination
all_list_elements = driver.find_elements(By.XPATH, '//*[@id="MainContent_tblRepeater"]/ul/li')
number_of_pages = len(all_list_elements)
number_of_pages

# Define the common part of the ID for the page number buttons
common_id_prefix = "MainContent_repeaterPaging_pagingLinkButton_"

# Initialize an empty DataFrame 
all_data = pd.DataFrame() 


# Loop through all pages
i = 0
while i <= number_of_pages - 1:
    # give some time to load
    time.sleep(3)

    # Locate the main table
    element = driver.find_element(By.CSS_SELECTOR, "#MainContent_gvSearch > tbody")

    table_html = element.get_attribute('outerHTML')

    soup = BeautifulSoup(table_html, 'html.parser')

    # Find and extract table rows
    rows = soup.find_all('tr')[1:]

    raw_data = []
    
    # Iterate through rows and extract data
    for row in rows:
        # Find and extract table cells (td or th elements)
        cells = row.find_all(['td', 'th'])
        row_data = [cell.text.strip() for cell in cells]
        
        # Append the cleaned data to the list
        raw_data.append(row_data)
    
    # convert to dataframe
    data = pd.DataFrame(raw_data)

    # Append the current page's data to the main DataFrame
    all_data = pd.concat([all_data, data], ignore_index=True, axis=0, sort=False)
    time.sleep(3)

    # Increment the page number and form the dynamic ID
    i += 1
    if i <= number_of_pages - 1:
        next_page_button_id = common_id_prefix + str(i)
        time.sleep(2)
        next_page = driver.find_element("id", next_page_button_id)
        next_page.click()
        time.sleep(4)

# Now, all_data contains data from all pages and save it as csv
all_data.to_csv("D:\LAND RA\python\data1.csv", index=False, encoding='utf-8-sig', float_format='%.0f')

