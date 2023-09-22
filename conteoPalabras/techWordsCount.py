## Conteo de palabras relacionadas con "datos" a partir de vacantes consultadas en ElEmpleo, Computrabajo, Indeed
## https://towardsdatascience.com/how-to-create-beautiful-word-clouds-in-python-cfcf85141214

import os
import sys
import time
import json
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

fecha_hoy = '20230920'
consec = time.strftime('20230920_%H%M%S', time.localtime())
# fecha_hoy = time.strftime('%Y%m%d', time.localtime())
# consec = time.strftime('%Y%m%d_%H%M%S', time.localtime())
path_portal = 'D:/LEARNING/PYTHON/webScrapingProjects/jobPortal/'
keywords = 'data,bi,dato,python,sql,azure,aws'

if not any(fecha_hoy in l for l in os.listdir('vacantes')):
    
    arch1 = subprocess.check_output([sys.executable, path_portal+"scr_computrabajo.py",'datos','','7',keywords])
    print(f"{arch1.strip().decode()}".replace('\\',"/"))

    arch2 = subprocess.check_output([sys.executable, path_portal+"scr_indeed.py",'datos','','7',keywords])
    print(f"{arch2.strip().decode()}".replace('\\',"/"))

    arch3 = subprocess.check_output([sys.executable, path_portal+"scr_elempleo.py",'datos','','hace-1-semana',keywords])
    print(f"{arch3.strip().decode()}".replace('\\',"/"))


## se comprueba si ya hay un json generado hoy
## si ya hay archivo, no se debe generar nuevamente
if any(fecha_hoy in l for l in os.listdir('json')):
    filename = [file for file in os.listdir('json') if fecha_hoy in file][0]

    jsonFile = open(f'json/{filename}','r')
    dict_frec = json.loads(jsonFile.read())
else:

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
    print(f'Lista de links generada con {len(urls_ls)} elementos..')


### --------------------------------------------------------------------------------------------
###                              THREADS
### --------------------------------------------------------------------------------------------
    print('Inicializando THREADS...')

    ## Threads falla si genera más de 100 hilos - se generan sublistas de 99 links máximo
    sub_lst_url = generar_sublistas(urls_ls,99)
    print(f'... se generan {len(sub_lst_url)} sublistas')

    ## threas

    lista_texto = []

    for lst in sub_lst_url:

        threads = []
        for link in lst:
            t = threading.Thread(target=get_text, args=(link,lista_texto,))
            threads.append(t)
            t.start()
            print(f".... se inicia hilo {t.name} para link {link}")

        for t in threads:
            t.join()


### --------------------------------------------------------------------------------------------
###                              CONTEO DE PALABRAS
### --------------------------------------------------------------------------------------------
    print('Inicializando CONTEO PALABRAS...')

    ## cargamos lista de palabrasde archivo
    file_ref = open('dataTechnologies.txt','r',encoding='utf-8-sig')
    tech_words = set()

    for line in file_ref.readlines():
            tech_words.add(line.strip().lower())


    ## concatenamos los textos
    comment_words = ' '.join(lista_texto)+' '
    comment_words = fn_replace_words(comment_words)
    comment_words = comment_words.split()

    # generamos diccionario de frecuencias
    dict_frec = {}
    for word in tech_words:
        c = comment_words.count(word)
        if c > 0:
            dict_frec[word] = c

    if not any(fecha_hoy in l for l in os.listdir('json')):
        dict_file = open(f'json/frec_{consec}.json','w')
        dict_file.write(json.dumps(dict_frec))
        print(f'... Diccionario de frecuencias "json/frec_{consec}.json" generado ')

## ----------------------------------   wordcount     

wordcloud = WordCloud(width = 800, 
                      height = 800,
                      max_words=50,
                      background_color ='white',
                      min_font_size = 10).generate_from_frequencies(dict_frec)


#--------------------------------- plot the WordCloud image                      
plt.figure(figsize = (10, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()