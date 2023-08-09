# JOB SCRAPING PROJECT  

En este proyecto se busca extraer información de vacantes de empleo desde algunos de los principales portales utilizados en Colombia. 
Para esto se construyó un Script de Python por cada página que se desee consultar, que son:  

* [Script de computrabajo](https://github.com/janickreales/webScrapingProjects/blob/main/jobPortal/scr_computrabajo.py)  
* [Script de Indeed](https://github.com/janickreales/webScrapingProjects/blob/main/jobPortal/scr_indeed.py)  
* [Script de ElEmpleo](https://github.com/janickreales/webScrapingProjects/blob/main/jobPortal/scr_elempleo.py)  

Los Scripts se irán modificando a medida que surjan nuevas necesidad. Por el momento el objetivo principal de crear estos scripts fue obtener información de algunas vacantes omitiendo toda la "basura" que suelen incluir los portales, además, automatizar el proceso de consulta de vacantes.   

Cada Script extrae la información de las vacantes publicadas para un cargo específico, en una ciudad indicada y con unos parámetros predeterminados. Luego los resultados se almacenan en un archivo .csv que cuenta con un consecutivo del día y hora exactos en que se creó. Esta información es finalmente levantada por un código ([sendEmail.py](https://github.com/janickreales/webScrapingProjects/blob/main/jobPortal/sendEmail.py)) que permite enviar un email a un destinatario deseado. La explicación de cómo se arma el correo está en los enlaces de las dos primeras líneas del script.  

Un último script ([send_JobEmail.py](https://github.com/janickreales/webScrapingProjects/blob/main/jobPortal/send_JobEmail.py)) se crea para pasar parámetros y unificar los scripts anteriores. Este se utiliza también para programar la tarea de envío del correo en el *programador de tareas* de windows. 



