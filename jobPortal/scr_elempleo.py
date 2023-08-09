#https://www.elempleo.com/co/

import os
import sys
import csv
import time
import math
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

root_page = 'https://www.elempleo.com'
main_page = 'https://www.elempleo.com/co/ofertas-empleo'


# ## Se define la URL que se pasará a Webdriver
def getUrl():
    cargo = sys.argv[1].replace(' ','-').lower()
    lugar = sys.argv[2].replace(' ','-').lower()
    fecha_post = sys.argv[3]

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
def get_job_info(page_source):
    # soup 
    soup = BeautifulSoup(page_source, 'html.parser')

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
    excluir = ['practicante','aprendiz','estudiante','enferm','obra','cocina','venta']
    keywords = sys.argv[4].split(',')
    return ((not any(excl in str.lower() for excl in excluir)) 
            and (any(keyword in str.lower() for keyword in keywords)))


def next_page():
    time.sleep(1)
    arrow = '.js-btn-next'
    arrow_click = driver.find_element(By.CSS_SELECTOR, arrow)

    try:
        arrow = '.js-btn-next'

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, arrow)))
        arrow_click.click()
    except:
        ActionChains(driver).move_to_element(arrow_click).click().perform()

## unificación 
def getJobs_elempleo():
    #aceptamos cookies 
    cookies()

    # vacantes primera página 
    job_lst = get_job_info(driver.page_source)

    ## vacantes encontradas
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        n = int(soup.find('strong',class_='js-total-results').text.strip())
        n_page = math.ceil(n/50)
    except:
        n_page = 0

    # siguientes páginas
    for i in range(n_page-1):
        # siguiente página
        next_page()        

        # agregamos a lista
        job_lst += get_job_info(driver.page_source)
    
    return job_lst


options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(getUrl())
time.sleep(2)


if __name__ == '__main__':
    # se aplica el filtro a las vacantes 
    dict_vacantes_v1 = getJobs_elempleo()
    
    try:
        dict_vacantes = [job for job in dict_vacantes_v1 if filterJobTitle(job['Titulo'])]
        claves = list(dict_vacantes[0].keys())

        ## creamos directorio para contener archivos si no existe
        if not os.path.exists('vacantes'):
            os.mkdir('vacantes')

        ## se crea un consecutivo (fecha_hora ejecución) y se crea csv
        consec = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        filename = f"vacantes/vacantes_elempleo_{sys.argv[1].replace(' ','-').lower()}_{consec}.csv"
        with open(filename,'w',newline='',encoding='utf-8-sig') as w:
            writer = csv.DictWriter(w,fieldnames=claves)
            writer.writeheader()
            writer.writerows(dict_vacantes)

        print(filename)
    except:
        print('')




driver.close()


