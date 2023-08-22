#!/usr/bin/env python3

# https://co.indeed.com/jobs

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
from funciones_varias import *

root_page = 'https://co.indeed.com'
keywords = sys.argv[4]


## se arma URL para el driver
def getUrl():
    cargo = sys.argv[1]
    lugar = sys.argv[2]
    fecha_act = sys.argv[3]


    root_url = 'https://co.indeed.com/jobs'
    params = {'q':cargo,'l':lugar,'fromage':fecha_act}
    page = requests.get(root_url, params=params)
    return page.url

### Función para cerrar ventanas emergentes
def handledPopUp(driver):
    time.sleep(2)
    popup = '.css-yi9ndv > svg:nth-child(1)'
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, popup)))
        close_popup = driver.find_element(By.CSS_SELECTOR, popup)
        close_popup.click()
    except:
        pass

### Función para navegar entre páginas
### Se utiliza para hacer "clic" en el botón ">" de Indeed
def next_page(driver):
    time.sleep(2)
    try:
        elem = driver.find_elements(By.CSS_SELECTOR,'.css-13p07ha.e8ju0x50')
        elem[-1].click()
    except:
        pass


## Se crea el objeto BeautifulSoup
def extract_soup(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup 


## Función para extraer la información básica a exportar
def get_job_info(soup):
    ## buscamos el tag "padre"
    elems = soup.find_all('div', class_='slider_item')

    ## agregamos las vacantes encontradas a una lista
    job_lst = []
    for elem in elems:
        href_ = elem.find('a')['href']
        href_ = f'{root_page}{href_}'

        job_lst.append({'Titulo': elem.find('a').text.strip(),
               'Empresa': elem.find('span',class_='companyName').text.strip(),
               'Ciudad': elem.find('div',class_='companyLocation').text.strip(),
               'Link': href_.strip(),
               'fecha_publicacion': get_time(elem.find('span',class_='date').text.strip())
                })

    return job_lst


def getJobs_Indeed():
    ## soup
    soup = extract_soup(driver.page_source)
    
    ## vacantes
    ## se extrae el valor del número de vacantes que encuentra la página
    try: 
        v_class = 'jobsearch-JobCountAndSortPane-jobCount css-1af0d6o eu4oa1w0'
        n_jobs = soup.find('div', class_= v_class).find('span')
        n = int(n_jobs.text.split(' ')[0])
    except:
        n=0

    n=12

    # se itera entra las páginas hasta alcanzar el # de vacantes n
    job_list = []
    while len(job_list)<n:
        start_time = time.time()

        # soup
        soup = extract_soup(driver.page_source)

        # se adjuntan las vacantes a una lista 
        job_list+=get_job_info(soup)

        #next_page 
        next_page(driver)

        # pop up
        time.sleep(2)
        handledPopUp(driver)

        # se sale si demora la iteración
        if (time.time() - start_time) > 15:
            break
    
    return job_list



options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(getUrl())
time.sleep(4)


if __name__ == '__main__':
    # se aplica el filtro a las vacantes 
    dict_vacantes_v1 = getJobs_Indeed()
    
    try:
        dict_vacantes = [job for job in dict_vacantes_v1 if filterJobTitle(job['Titulo'],keywords)]
        claves = list(dict_vacantes[0].keys())

        ## creamos directorio para contener archivos si no existe
        if not os.path.exists('vacantes'):
            os.mkdir('vacantes')

        ## se crea un consecutivo (fecha_hora ejecución) y se crea csv
        consec = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        filename = f"vacantes/vacantes_indeed_{sys.argv[1].replace(' ','-').lower()}_{consec}.csv"
        with open(filename,'w',newline='',encoding='utf-8-sig') as w:
            writer = csv.DictWriter(w,fieldnames=claves,delimiter=';')
            writer.writeheader()
            writer.writerows(dict_vacantes)

        print(filename)
    except:
        print('')

driver.close()
