import os
import sys
import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

root_page = 'https://www.elempleo.com'
main_page = 'https://www.elempleo.com/co/ofertas-empleo'

def getUrl():
    cargo = 'psicologo' #sys.argv[1].replace(' ','-').lower()
    lugar = '' #sys.argv[2].replace(' ','-').lower()
    fecha_post = 'hace-1-semana'

    url = f'{main_page}/{lugar}/{fecha_post}'
    page = requests.get(url, params={'trabajo':cargo})

    return page.url

## Aceptar cookies
def cookies():
    cookies_xpath = '/html/body/div[10]/div/div[2]/a'

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cookies_xpath)))
    close_cookies = driver.find_element(By.XPATH, cookies_xpath)
    close_cookies.click()



options = Options()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(getUrl())

time.sleep(1)


## obtener empleos
soup = BeautifulSoup(driver.page_source, 'html.parser')

cookies()
time.sleep(1)

## clickear


arrow = '.js-btn-next'

c = 1
while c != 0:
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, arrow)))
        next_page = driver.find_element(By.CSS_SELECTOR, arrow)
        next_page.click()

        print(c)
    except:
        c = 0
        print(c)
