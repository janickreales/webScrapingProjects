import os
import sys
import time
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import requests
from bs4 import BeautifulSoup
import threading

# from funciones_varias import *

keywords_psico = 'psicolo,psicól,recursos,gener,human,social,selec'
keywords_aux = 'admin,recursos,gener,human,auxil,asist'
vacantes = {'psicologia':keywords_psico,'auxiliar administrativa':keywords_aux}

#argumentos para subprocess --> 'posición buscada','ciudad','fecha_actualización','palabras clave', '1:0' extraer:no extraer texto
# for vacante,keywords in vacantes.items():
    
#     # OBTENEMOS EL NOMBRE DEL ÚLTIMO ARCHIVO DE VACANTES GENERADO PARA CADA PÁGINA
# path_portal = 'D:/LEARNING/PYTHON/webScrapingProjects/jobPortal/'
# arch1 = subprocess.check_output([sys.executable, path_portal+"scr_computrabajo.py",'datos','medellin','1','data,bi,datos','1'])
# ruta1 = f"{os.getcwd()}/{arch1.strip().decode()}".replace('\\',"/")

    # arch2 = subprocess.check_output([sys.executable, path_portal+"scr_indeed.py",vacante,'medellin','3',keywords])
    # ruta2 = f'{os.getcwd().replace("\\","/")}/{arch2.strip().decode()}'

    # arch3 = subprocess.check_output([sys.executable, path_portal+"scr_elempleo.py",vacante,'medellin','hoy',keywords])
    # ruta3 = f'{os.getcwd().replace("\\","/")}/{arch3.strip().decode()}'
    
    ## se concatenan las rutas
    # ruta_archivo = ruta1+','+ruta2+','+ruta3
    
    # print(f'Archivos de vacantes para "{vacante}" generados')
# print(ruta1)

file_ref = open('dataTechnologies.txt','r',encoding='utf-8-sig')
tech_words = set()

for line in file_ref.readlines():
        tech_words.add(line.strip().lower())


### ------------------------------------------------------------------------------------------

# ruta1 = f"{os.getcwd()}/vacantes/vacantes_computrabajo_auxiliar-administrativa_20230815_161711.csv".replace('\\',"/")
ruta1 = 'D:/LEARNING/PYTHON/webScrapingProjects/conteoPalabras/vacantes/vacantes_elempleo_datos_20230816_193146_1.csv'
df_compu = pd.read_csv(ruta1,delimiter=';')
urls_ls = list(df_compu.Link)

## Función para entrar a cada vacante y extraer el tag del salario. 
## Se puede adecuar para extraer cualquier otra información (como descripción...)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}

lista2 = []
def get_text(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text,'html.parser')

    texto = soup.find('div',class_='description-block').find('p')
    lista2.append(texto.text.strip().lower())

    return texto.text



t0 = time.time()

threads = []
for link in urls_ls:
    t = threading.Thread(target=get_text, args=(link,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

tf = time.time()-t0
print(f'tiempo total con hilos: {tf}')


comment_words = ' '.join(lista2)+' '
comment_words = comment_words.replace('english','inglés')
# --------------------------------------------------------------------------------------------------------------------------

dict1 = {}
for word in tech_words:
     c = comment_words.count(word)
     if c > 0:
        dict1[word] = c

print(dict1)




#####----------------------------------------------------------------------------------
# comment_words = ''
stopwords = set(STOPWORDS)


# for val in df_compu.texto:
     
#     # typecaste each val to string
#     val = str(val)
 
#     # split the value
#     tokens = val.split()
     
#     # Converts each token into lowercase
#     for i in range(len(tokens)):
#         tokens[i] = tokens[i].lower()
     
#     comment_words += " ".join(tokens)+" "

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                # stopwords = stopwords,
                min_font_size = 10).generate_from_frequencies(dict1)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()

