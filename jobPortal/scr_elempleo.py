#https://www.elempleo.com/co/

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

# ## Se define la URL que se pasará a Webdriver
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

## Función para extraer la información básica a exportar
def get_job_info(soup):
    ## buscamos el tag "padre"
    elems = soup.find_all('div', class_='result-item')

    ## agregamos las vacantes encontradas a una lista
    job_lst = []
    for elem in elems:
        href_ = elem.find('a')['href'].strip()
        p_date = elem.find('span',class_='info-publish-date').text.strip()
        p_date = p_date.replace('Publicado ','')

        job_lst.append({'Titulo': elem.find('a').text.strip(),
               'Empresa': elem.find('span',class_='info-company-name').text.strip(),
               'Ciudad': elem.find('span',class_='info-city').text.strip(),
               'Link': f'{root_page}{href_}',
               'fecha_publicacion': f'{p_date}'
                })

    return job_lst

## Se filtran los títulos de vacantes que cumplan con ciertas caractarísticas
def filterJobTitle(str):
    excluir = ['practicante','aprendiz','estudiante']
    keywords = sys.argv[4].split(',')
    return ((not any(excl in str.lower() for excl in excluir)) 
            and (any(keyword in str.lower() for keyword in keywords)))


def next_page():
    arrow = '.js-btn-next'

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, arrow)))
    next_page = driver.find_element(By.CSS_SELECTOR, arrow)
    next_page.click()

## unificación 
def getJobs_elempleo():

    #aceptamos cookies 
    cookies()
    time.sleep(1)

    # soup 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_lst = get_job_info(soup)

    ## vacantes encontradas
    try:
        total = soup.find('strong',class_='js-total-results').text.strip()
        n = int(total)
    except:
        n = 0

    print(n)

    while len(job_lst) <= n:
        # siguiente página
        next_page()

        # soup 
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # agregamos a lista
        job_lst += get_job_info(soup)
    
    return job_lst


options = Options()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(getUrl())

jobs = getJobs_elempleo()

print(len(jobs))





# driver.close()


