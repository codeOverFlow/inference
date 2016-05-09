#coding:utf-8
from Classe_Automate import *
from L_star import *

from os import listdir
from os.path import isfile, join

import datetime

# Tests (Victor)
#automate1 = Automate.importFromFile("DataAutomate/141_Cambodian.fsa.att")

mypath = "DataAutomate"

for f in listdir(mypath):
    if isfile(join(mypath, f)) and f!="202_Piraha.fsa.att":
        a = Automate.importFromFile(join(mypath, f))
        print f
        #print a
        
        oracle = Oracle(a)
        alphabet = a.getAlphabet()
        l_star = L_star(alphabet, oracle)
    
        #debut = datetime.datetime.now()
        
        l_star.run()
        #l_star.run_without_equivalence()
        
        #fin = datetime.datetime.now()
        
        #print "Durée : ", fin-debut
        print