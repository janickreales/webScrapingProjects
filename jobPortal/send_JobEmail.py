
### ESTE SCRIPT EJECUTA LA GENERACIÓN DEL ARCHIVO CON LAS VACANTES DE COMPUTRABAJO E INDEED GENERADAS PARA LOS ÚLTIMOS 3 DÍAS
### LUEGO LEVANTA LA RUTA DEL ARCHIVO Y LO PASA COMO ARGUMENTO DEL SCRIPT QUE ENVÍA EL CORREO
### SE DEJAN QUEMADAS LAS VACANTES QUE SE QUIEREN BUSCAR EN CADA PÁGINA

import os
import sys
import subprocess

keywords_psico = 'psicolo,psicól,recursos,gener,human,social,selec'
keywords_aux = 'admin,recursos,gener,human,auxil'
vacantes = {'psicologia':keywords_psico,'auxiliar administrativa':keywords_aux}

#argumentos para subprocess --> 'posición buscada','ciudad','fecha_actualización','palabras clave'
for vacante,keywords in vacantes.items():
    
    ## OBTENEMOS EL NOMBRE DEL ÚLTIMO ARCHIVO DE VACANTES GENERADO PARA CADA PÁGINA
    # os.chdir('/mnt/d/LEARNING/PYTHON/webScrapingProjects/jobPortal')
    os.chdir('D:/LEARNING/PYTHON/webScrapingProjects/jobPortal')
    arch1 = subprocess.check_output([sys.executable, "scr_computrabajo.py",vacante,'medellin','3',keywords])
    ruta1 = f'D:/LEARNING/PYTHON/webScrapingProjects/jobPortal/{arch1.strip().decode()}'
    
    arch2 = subprocess.check_output([sys.executable, "scr_indeed.py",vacante,'medellin','3',keywords])
    ruta2 = f'D:/LEARNING/PYTHON/webScrapingProjects/jobPortal/{arch2.strip().decode()}'
    
    if 'vacantes' in arch2.strip().decode():
        ruta_archivo = ruta1+','+ruta2
    else:
        ruta_archivo = ruta1
    
    print(f'Archivos de vacantes para "{vacante}" generados')


    ## VAMOS A LA CARPETA DEL SCRIPT QUE ENVÍA EL CORREO
    # os.chdir('/mnt/d/LEARNING/PYTHON/emailing')
    os.chdir('D:/LEARNING/PYTHON/emailing')
    r2 = subprocess.run([sys.executable, "send_email.py",vacante,ruta_archivo])
    print(f'Archivos de vacantes para "{vacante}" enviados')




