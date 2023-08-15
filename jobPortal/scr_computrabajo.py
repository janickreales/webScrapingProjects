#!/usr/bin/env python3

# https://co.computrabajo.com/

import os
import sys
import csv
import time
import requests
from bs4 import BeautifulSoup
from funciones_varias import *

main_page = 'https://co.computrabajo.com'
keywords = sys.argv[4]

## Se define la URL que se pasará a Request (depende de si se pasa un lugar como argumento)
def getUrl():
    # cargo = input('Ingrese el cargo requerido: ').replace(' ','-').lower()
    # lugar = input('Ingrese ciudad (opcional): ').replace(' ','-').lower()
    cargo = sys.argv[1].replace(' ','-').lower()
    lugar = sys.argv[2].replace(' ','-').lower()

    if lugar == '':
        url = f'{main_page}/trabajo-de-{cargo}'
    else:
        url = f'{main_page}/trabajo-de-{cargo}-en-{lugar}'

    return url

## Se definen los parámetros a pasar al Requests
# se dejan vacíos todos los parámetros
# En instrucciones.txt se indican los valores con los que pueden llenarse
def getParams(p=''):
    sal = '' #input('Rango salarial: ')
    iex = '' #input('Años de experiencia: ')
    pubdate = sys.argv[3] #input('Fecha actualización: ')
    cont = '' #input('Tipo contrato: ')
    
    params = {'sal':sal,'iex':iex,'pubdate':pubdate,'cont':cont,'p':p}
    params = {k:params[k] for k in params if params[k]!=''}

    return params

## Se crea el objeto BeautifulSoup
def extract_soup(url,params={}):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    page = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(page.text, 'html.parser')

    return soup

## Función para entrar a cada vacante y extraer el tag del salario. 
## Se puede adecuar para extraer cualquier otra información (como descripción...)
def extract_salario(link):
    soup = extract_soup(link)
    oferta = soup.find('div', attrs={'div-link':'oferta'})

    salario = oferta.find('span').text
    # texto = oferta.find('p').text

    return salario


## Función para extraer la información básica a exportar
def get_job_info(soup):
    ## buscamos el tag "padre"
    elems = soup.find_all('article', class_='box_offer')

    ## agregamos las vacantes encontradas a una lista
    job_lst = []
    for elem in elems:
        data_compl = elem.find('p').text.strip().split('\n')
        href_ = elem.find('a')['href']
        href_ = f'{main_page}{href_}'

        job_lst.append({'Titulo': elem.find('h2').text.strip(),
               'Empresa': data_compl[0].strip(),
               'Ciudad': data_compl[-1].strip(),
               'Link': href_.strip(),
               'fecha_publicacion': get_time(elem.find('p',class_='fs13').text.strip()),
                })

    return job_lst


 ## Se integra todo el proceso   
def getInfo():
    ### Inputs
    url = getUrl()
    params = getParams()
    soup = extract_soup(url,params)

    ### cantidad de vacantes encontradas
    h1 = soup.find('h1', class_='title_page').find('span')
    n = int(h1.text.replace('.',''))

    i = 1
    job_list = []
    
    #Se llena job_list hasta que se alcance el # total de vacantes que arroja la página
    while len(job_list) < n:
        params['p']=i
        soup = extract_soup(url,params)
        job_list+=get_job_info(soup)

        i+=1

    return job_list


if __name__ == '__main__':
    # start_time = time.time()
    dict_vacantes_v1 = getInfo()
    
    dict_vacantes = [job for job in dict_vacantes_v1 if filterJobTitle(job['Titulo'],keywords)]
    claves = list(dict_vacantes[0].keys())

    ## creamos directorio para contener archivos si no existe
    if not os.path.exists('vacantes'):
        os.mkdir('vacantes')

    ## se crea un consecutivo (fecha_hora ejecución) y se crea csv
    consec = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    filename = f"vacantes/vacantes_computrabajo_{sys.argv[1].replace(' ','-').lower()}_{consec}.csv"
    with open(filename,'w',newline='',encoding='utf-8-sig') as w:
        writer = csv.DictWriter(w,fieldnames=claves)
        writer.writeheader()
        writer.writerows(dict_vacantes)

    print(filename)
