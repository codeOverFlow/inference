#coding:utf-8
from Classe_Automate import *
from L_star import *

from os import listdir
from os.path import isfile, join
            

a = Automate.importFromFile("DataAutomate/141_Cambodian.fsa.att")

oracle = Oracle(a)
alphabet = a.getAlphabet()
l_star = L_star(alphabet, oracle)


#l_star.run()
l_star.run_without_equivalence()

