import requests
import threading
import concurrent.futures
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}

## extrae texto de vacantes de computrabajo,elempleo o indeed
def get_text(url,lista=[]):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text,'html.parser')

    try:
        if 'computrabajo' in url:
            texto = soup.find('div',attrs={'div-link':'oferta'}).find('p',class_='mbB').text
        elif 'indeed' in url:
            texto = soup.find('div',id='jobDescriptionText').text
        else:
            texto = soup.find('div',class_='description-block').find('p').text
    except:
        texto = ''

    lista.append(texto.strip().lower())

    return texto


## función para generar sublistas
## recibe una lista y el tamaño (n) máximo de cada sublista
def generar_sublistas(lista, n):
    sublistas = []
    for i in range(0, len(lista), n):
        sublista = lista[i:i+n]
        sublistas.append(sublista)
    return sublistas