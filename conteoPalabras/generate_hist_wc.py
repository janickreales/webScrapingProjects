import os
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud

### FUNCIÓN PARA CARGAR TODOS ARCHIVOS JSON GENERADOS POR "techWordsCount.py" DE LA RUTA "JSON"
### LOS AGREGA A UNA LISTA Y SUMARIZA LAS CLAVES
### GENERA UN DICCIONARIO "AGREGADO" DE LA FRECUENCIA CON QUE APARECEN LAS CLAVES EN LAS OFERTAS DE EMPLEO

def cargar_y_concatenar_json_en_ruta(ruta):
    datos_concatenados = []
    dict_frec = {}

    # Enumerar archivos en la ruta
    for archivo in os.listdir(ruta):
        if archivo.endswith(".json"):
            archivo_path = os.path.join(ruta, archivo)
            
            # Leer y cargar el archivo JSON
            with open(archivo_path, "r") as json_file:
                try:
                    datos = json.load(json_file)
                    datos_concatenados.append(datos)
                except json.JSONDecodeError as e:
                    print(f"Error al cargar {archivo}: {str(e)}")

    # concatenar diccionarios
    for d in datos_concatenados:
        for k,v in d.items():
            if k in dict_frec:
                dict_frec[k] += v
            else:
                dict_frec[k] = v
        
    return dict_frec


## ----------------------------------   wordcount     
dict_frec = cargar_y_concatenar_json_en_ruta('json')

wordcloud = WordCloud(width = 800, 
                      height = 800,
                      max_words=35,
                      background_color ='white',
                      min_font_size = 10).generate_from_frequencies(dict_frec)


#--------------------------------- plot the WordCloud image                      
plt.figure(figsize = (10, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()