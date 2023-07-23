
#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
import sys


url = 'https://co.indeed.com/jobs'
params = {'q':'psicologa','l':'medellin'}
page = requests.get(url, params=params)
main_page = page.url
# main_page = 'https://co.indeed.com/jobs?q=psicologa&l=Medell%C3%ADn%2C+Antioquia&start=20&pp=gQAeAAAAAAAAAAAAAAACCtbXLwAdAQEBByvjyEk1BoF1GoK72bJRoTJehYWR8tyCRvsAAA&vjk=8181d0d861462a42'


def next_page(driver):
    try:
        elem = driver.find_elements(By.CSS_SELECTOR,'.css-13p07ha.e8ju0x50')
        elem[-1].click()

        print('Next page')
    except:
        print('No next page')


def handledPopUp(driver):
    popup = '.css-yi9ndv > svg:nth-child(1)'
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, popup)))
        close_popup = driver.find_element(By.CSS_SELECTOR, popup)
        close_popup.click()

        print(f'Pop Up cerrado')
    except:
        print(f'Pop Up no apareció')


def getUrl():
    cargo = sys.argv[1].replace(' ','-').lower()
    lugar = sys.argv[2].replace(' ','-').lower()


    root_url = 'https://co.indeed.com/jobs'
    params = {'q':cargo,'l':lugar}
    page = requests.get(root_url, params=params)
    return page.url

print(getUrl())

