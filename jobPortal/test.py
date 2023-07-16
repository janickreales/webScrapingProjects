
#!/usr/bin/env python3

import sys

# print(sys.argv[1].split(','))

def filterJobTitle(str):
    keywords = sys.argv[1].split(',')
    return any(keyword in str.lower() for keyword in keywords)

ls_1 = [{'titulo':'el amor de los recuerdos','vacante':'la vaina'},{'titulo':'paquita gallego','vacante':'agugu tata'}]
texto = 'el amor de los recuerdos'
print([elem for elem in ls_1 if filterJobTitle(elem['titulo'])])