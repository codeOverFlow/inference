import math
from Classe_Automate import *
import numpy as np

def distanceEuclidean(automate1, automate2):
    print "C", coem(automate1, automate1), coem(automate2, automate2), coem(automate1, automate2)
    return math.sqrt(coem(automate1, automate1) + coem(automate2, automate2) -2 * coem(automate1, automate2))
    
def coem(automate1, automate2):
    somme = 0
    
    index, n = calculAllN(automate1, automate2)
    
    for k1 in automate1.automaton:
        for k2 in automate2.automaton:
            probF1 = 1 if k1 in automate1.endingState else 0
            probF2 = 1 if k2 in automate2.endingState else 0
            somme += n[index[(k1,k2)]]*probF1*probF2
            
    return somme
    
def calculAllN(automate1, automate2):
    equaN = []
    resN = []
    indexN = {}
    for k1 in automate1.automaton:
        for k2 in automate2.automaton:
            probStart1 = 1 if k1 in automate1.startingStates else 0
            probStart2 = 1 if k2 in automate2.startingStates else 0
            
            indexN[(k1, k2)] = len(equaN)
            equaN.append([0]*(len(automate1.automaton.keys())* len(automate2.automaton.keys())))
            resN.append(-probStart1*probStart2)
    #print automate1.getAlphabet()
    #print automate2.getAlphabet()
    assert(set(automate1.getAlphabet()) == set(automate2.getAlphabet()))
    for k1 in automate1.automaton:
        for k2 in automate2.automaton:
            for q1 in automate1.automaton:
                for q2 in automate2.automaton:
                    for a in automate1.getAlphabet():
                        nbTransFromQ1 = len([(s,e,t) for s,v in automate1.automaton.iteritems() for (e,t) in v if s == q1])
                        probA1 = float(len([(s,e,t) for s,v in automate1.automaton.iteritems() for (e,t) in v if s == q1 and e == k1 and t == a]))/float(nbTransFromQ1) if nbTransFromQ1 != 0 else 0
            
                        nbTransFromQ2 = len([(s,e,t) for s,v in automate2.automaton.iteritems() for (e,t) in v  if s == q2])
                        probA2 = float(len([(s,e,t) for s,v in automate2.automaton.iteritems() for (e,t) in v  if s == q2 and e == k2 and t == a]))/float(nbTransFromQ2) if nbTransFromQ2 != 0 else 0
                        
                        equaN[indexN[(k1,k2)]][indexN[(q1,q2)]] = probA1 * probA2
                        equaN[indexN[(k1,k2)]][indexN[(k1,k2)]] -= 1
                        
    a = np.array(equaN)
    b = np.array(resN)
    x = np.linalg.solve(a,b)
    
    return (indexN, x)
    
def testEquivalence(automate1, automate2):
    return distanceEuclidean(automate1, automate2) == 0

if __name__ == '__main__':
    automate1 = Automate.importFromFile("DataAutomate/141_Cambodian.fsa.att")
    automate2 = Automate.importFromFile("DataAutomate/189_Maori.fsa.att")
    
    automate3 = Automate.importFromFile("DataAutomate/154_English.fsa.att")
    automate4 = Automate.importFromFile("DataAutomate/152_Dutch_SPD.fsa.att")
    automate5 = Automate.importFromFile("DataAutomate/122_Arabic_Classical_SPD.fsa.att")
    
    print distanceEuclidean(automate3, automate4)
    print distanceEuclidean(automate3, automate5)
    print distanceEuclidean(automate4, automate5)

