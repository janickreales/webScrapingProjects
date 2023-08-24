## Conteo de palabras relacionadas con "datos" a partir de vacantes consultadas en ElEmpleo, Computrabajo, Indeed

import os
import sys
import time
import requests
import threading
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from funciones_varias import *



### --------------------------------------------------------------------------------------------
###                     GENERACIÓN DE ARCHIVOS DE VACANTES PARA ÚLTIMOS 7 DÍAS
### --------------------------------------------------------------------------------------------

## Comprobación si ya hay archivos generados de la fecha

fecha_hoy = '20230823' #time.strftime('%Y%m%d', time.localtime())
consec = time.strftime('%Y%m%d_%H%M%S', time.localtime())
path_portal = 'D:/LEARNING/PYTHON/webScrapingProjects/jobPortal/'
keywords = 'data,bi,dato,python,sql,azure,aws'

if not any(fecha_hoy in l for l in os.listdir('vacantes')):
    
    arch1 = subprocess.check_output([sys.executable, path_portal+"scr_computrabajo.py",'datos','medellin','7',keywords])
    print(f"{arch1.strip().decode()}".replace('\\',"/"))

    arch2 = subprocess.check_output([sys.executable, path_portal+"scr_indeed.py",'datos','medellin','7',keywords])
    print(f"{arch2.strip().decode()}".replace('\\',"/"))

    arch3 = subprocess.check_output([sys.executable, path_portal+"scr_elempleo.py",'datos','medellin','hace-1-semana',keywords])
    print(f"{arch3.strip().decode()}".replace('\\',"/"))


### --------------------------------------------------------------------------------------------
###                                  GENERACIÓN DATAFRAMES
### --------------------------------------------------------------------------------------------

## lista archivos generados en la fecha
csv_files = [file for file in os.listdir('vacantes') if fecha_hoy in file]

## lista dataframes
dataframes = []

for file in csv_files:
    df = pd.read_csv('vacantes/'+file,delimiter=';')
    dataframes.append(df[['Titulo','Link']])

# Concatenar los DataFrames en uno solo
df_final = pd.concat(dataframes, ignore_index=True)

# lista de links
urls_ls = list(df_final.Link)


### --------------------------------------------------------------------------------------------
###                              THREADS
### --------------------------------------------------------------------------------------------


## Threads falla si genera más de 100 hilos - se generan sublistas de 99 links máximo
sub_lst_url = generar_sublistas(urls_ls,99)

## threas

lista_texto = []

for lst in sub_lst_url:

    threads = []
    for link in lst:
        t = threading.Thread(target=get_text, args=(link,lista_texto,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


### --------------------------------------------------------------------------------------------
###                              CONTEO DE PALABRAS
### --------------------------------------------------------------------------------------------

## cargamos lista de palabrasde archivo
file_ref = open('dataTechnologies.txt','r',encoding='utf-8-sig')
tech_words = set()

for line in file_ref.readlines():
        tech_words.add(line.strip().lower())


## concatenamos los textos
comment_words = ' '.join(lista_texto)+' '
comment_words = comment_words.replace('english','inglés')

# generamos diccionario de frecuencias
dict_frec = {}
for word in tech_words:
     c = comment_words.count(word)
     if c > 0:
        dict_frec[word] = c

dict_file = open(f'json/frec_{consec}.json','w')
dict_file.write(str(dict_frec))

## ----------------------------------   wordcount     

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate_from_frequencies(dict_frec)


#--------------------------------- plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()



