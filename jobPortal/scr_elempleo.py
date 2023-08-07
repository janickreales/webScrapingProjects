#https://www.elempleo.com/co/

import os
import sys
import csv
import time
import requests
from bs4 import BeautifulSoup


main_page = 'https://www.elempleo.com/co/ofertas-empleo/'

# ## Se define la URL que se pasará a Request
# def getUrl():
#     # cargo = input('Ingrese el cargo requerido: ').replace(' ','-').lower()
#     # lugar = input('Ingrese ciudad (opcional): ').replace(' ','-').lower()
#     cargo = sys.argv[1].replace(' ','-').lower()
#     lugar = sys.argv[2].replace(' ','-').lower()

#     if lugar == '':
#         url = f'{main_page}/{lugar}'
#     else:
#         url = f'{main_page}/trabajo-de-{cargo}-en-{lugar}'

#     return url

params = {'trabajo':'ingeniero de datos'}

page = requests.get(main_page, params=params)

print(page.url)