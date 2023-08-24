
## librerías
from datetime import datetime, timedelta
    

## obtener fecha de publicación formateada
def get_time(d_str):
    p_hoy = ['hora','recien','recién','hoy','minuto','seg']

    if any(p in d_str.lower() for p in p_hoy):
        d = 0
    elif 'ayer' in d_str.lower():
        d = 1
    else:
        try:
            d = int(d_str.strip().split(' ')[-2])
        except:
            d = 0

    f = datetime.today() - timedelta(days=d)
    f_string = f.strftime('%Y-%m-%d')

    return f_string


## filtro vacantes empleo por keywords
def filterJobTitle(str,keywords):
    excluir = ['practicante','aprendiz','estudiante','enferm','obra','cocina','venta','agente','call']
    keywords = keywords.split(',')
    return ((not any(excl in str.lower() for excl in excluir)) 
            and (any(keyword in str.lower() for keyword in keywords)))
