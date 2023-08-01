import os
import sys
import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Firefox(executable_path="/mnt/d/LEARNING/PYTHON/webScrapingProjects/geckodriver.exe",options=options)
driver = webdriver.Firefox()
driver.get('https://co.indeed.com/jobs?q=psicologo&l=Medell%C3%ADn%2C+Antioquia&fromage=3&vjk=edfc1a52e66f3192')
time.sleep(3)



soup = BeautifulSoup(driver.page_source, 'html.parser')

## vacantes
v_class = 'jobsearch-JobCountAndSortPane-jobCount css-1af0d6o eu4oa1w0'
n_jobs = soup.find('div', class_= v_class).find('span')
n = int(n_jobs.text.split(' ')[0])

print(n)
