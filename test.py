from Main import txtToListe
import os
from form import customer
a = customer('iyad','hadife','dad','dadad')
print(a.get_email())
print(a.get_password())

data = 'FinalProjectPython\PoubelleDepatel\customer.txt'
txtToListe(data)