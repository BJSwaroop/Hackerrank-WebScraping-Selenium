import selenium
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
import requests
# import mysql.connector as connector
driver = webdriver.Chrome(ChromeDriverManager().install())
# def fetch_page(link)
# p = 1
driver.get('https:/www.gmail.com')
am = driver.find_element_by_name("identifier")
am.send_keys("bjepic200009@gmail.com")
driver.find_element_by_css_selector("#identifierNext > div > button").click()

# driver.get('https://mail.google.com/mail/u/0/#inbox?compose=new')

