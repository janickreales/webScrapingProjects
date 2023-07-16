
#!/usr/bin/env python3

import sys

# print(sys.argv[1].split(','))

testo = 'el amor de los recuerdos'
pala = ['ant','amod']

if any(p in testo for p in pala):
    print('aja')
else:
    print('uh uh')