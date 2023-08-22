
### ESTE SCRIPT EJECUTA LA GENERACIÓN DEL ARCHIVO CON LAS VACANTES DE COMPUTRABAJO E INDEED GENERADAS PARA LOS ÚLTIMOS 3 DÍAS
### LUEGO LEVANTA LA RUTA DEL ARCHIVO Y LO PASA COMO ARGUMENTO DEL SCRIPT QUE ENVÍA EL CORREO
### SE DEJAN QUEMADAS LAS VACANTES QUE SE QUIEREN BUSCAR EN CADA PÁGINA

import os
import sys
import subprocess

keywords_psico = 'psicolo,psicól,recursos,gener,human,social,selec'
keywords_aux = 'admin,recursos,gener,human,auxil,asist'
vacantes = {'psicologia':keywords_psico,
            'auxiliar administrativa':keywords_aux}

#argumentos para subprocess --> 'posición buscada','ciudad','fecha_actualización','palabras clave'
for vacante,keywords in vacantes.items():
    
    ## OBTENEMOS EL NOMBRE DEL ÚLTIMO ARCHIVO DE VACANTES GENERADO PARA CADA PÁGINA
    # os.chdir('/mnt/d/LEARNING/PYTHON/webScrapingProjects/jobPortal')
    # os.chdir('D:/LEARNING/PYTHON/webScrapingProjects/jobPortal')
    path_portal = 'D:/LEARNING/PYTHON/webScrapingProjects/jobPortal/'
    arch1 = subprocess.check_output([sys.executable, path_portal+"scr_computrabajo.py",vacante,'medellin','3',keywords])
    ruta1 = f'{path_portal}{arch1.strip().decode()}'
    
    arch2 = subprocess.check_output([sys.executable, path_portal+"scr_indeed.py",vacante,'medellin','3',keywords])
    ruta2 = f'{path_portal}{arch2.strip().decode()}'

    arch3 = subprocess.check_output([sys.executable, path_portal+"scr_elempleo.py",vacante,'medellin','hoy',keywords])
    ruta3 = f'{path_portal}{arch3.strip().decode()}'
    
    ## se concatenan las rutas
    ruta_archivo = ruta1+','+ruta2+','+ruta3
    
    print(f'Archivos de vacantes para "{vacante}" generados')


    # VAMOS A LA CARPETA DEL SCRIPT QUE ENVÍA EL CORREO
    # os.chdir('/mnt/d/LEARNING/PYTHON/emailing')
    # os.chdir('D:/LEARNING/PYTHON/emailing')
    path_email = 'D:/LEARNING/PYTHON/emailing/'
    r2 = subprocess.run([sys.executable, path_email+"send_email.py",vacante,ruta_archivo])
    print(f'Archivos de vacantes para "{vacante}" enviados')




