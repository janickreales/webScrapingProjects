
### ESTE SCRIPT EJECUTA LA GENERACIÓN DEL ARCHIVO CON LAS VACANTES DE COMPUTRABAJO GENERADAS PARA EL DÍA DE HOY
### LUEGO LEVANTA LA RUTA DEL ARCHIVO Y LO PASA COMO ARGUMENTO DEL SCRIPT QUE ENVÍA EL CORREO
### SE DEJAN QUEMADAS LAS VACANTES QUE SE QUIEREN BUSCAR

import os
import sys
import subprocess

keywords_psico = 'psicolo,psicól,recursos,gener,human'
keywords_aux = 'admin,recursos,gener,human,auxil'
vacantes = {'psicologia':keywords_psico,'auxiliar administrativa':keywords_aux}

# argumentos para subprocess --> 'posición buscada','ciudad','fecha_actualización','palabras clave'
for vacante,keywords in vacantes.items():
    
    ## Obtenemos el nombre del último archivo generado
    os.chdir('/mnt/d/LEARNING/PYTHON/webScrapingProjects/jobPortal')
    nombre_arch = subprocess.check_output([sys.executable, "scr_computrabajo.py",vacante,'medellin','1',keywords])
    ruta_archivo = f'/mnt/d/LEARNING/PYTHON/webScrapingProjects/jobPortal/{nombre_arch.strip().decode()}'
    print(f'Archivo de vacantes para "{vacante}" generado')

    ## nos dirigimos a la carpeta del script que envía el correo
    os.chdir('/mnt/d/LEARNING/PYTHON/emailing')
    r2 = subprocess.check_output([sys.executable, "send_email.py",vacante,ruta_archivo])
    print(f'Archivo de vacantes para "{vacante}" enviado')