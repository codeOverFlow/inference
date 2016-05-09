#coding:utf-8

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random

from os import listdir
from os.path import isfile, join

#Supposition : un seul état initial et déterministe

class Automate:
    
    def getAlphabet(self):
        return [a+'.'+b for a in ['w0', 'w1', 'w2', 'w3', 's4'] for b in ['s0', 's1', 's2']]
        #return self.alphabet
        
    def __init__(self):
        # L'automate est initialisé vide
        # L'automate est représenté par un dictionnaire 
        # {étatdepart : (état_arrivé, (w, s))}

        self.automaton = {}
        self.startingStates = []
        self.endingState = []
        self.alphabet = []
        
    def addState(self, name, isStarting=False, isFinal=False):
        if name not in self.automaton:
            self.automaton[name] = []
            if isStarting:
                self.startingStates.append(name)
            if isFinal:
                self.endingState.append(name)
            
    def setStateInitial(self, statename):
        if statename in self.automaton:
            self.startingStates.append(statename)
        else:
            print("StateInit : State does not exist")
     
    def setStateFinal(self, statename):
        if statename in self.automaton:
            self.endingState.append(statename)
        else:
            print("State final : State does not exist")   
    
    def removeState(self, name):
        del self.automaton[name]
        if name in self.startingStates:
            self.startingStates.remove(name)
        if name in self.endingState:
            self.endingState.remove(name)
    
    def addTransition(self, statename1, statename2, transname):
        if not statename1 in self.automaton:
            self.automaton[statename1] = []
        if not (statename2, transname) in self.automaton[statename1]:
            self.automaton[statename1].append((statename2, transname))
        if transname not in self.alphabet:
            self.alphabet.append(transname)
        
    def removeTransition(self, statename1, statename2, transname):
        self.automaton[statename1].remove((statename2, transname))
        
    def isWasteState(self, state):
        #Ne gère pas les cas de multiples états non accepteurs (genre boucle infinie)
        if state in self.endingState:
            return False
            
        for s in self.automaton[state]:
            if s[0] != state:
                return False
    
        return True
        
    def generate(self):
        state = self.startingStates[random.randint(0, len(self.startingStates)-1)]
        
        res = ""
        
        while(True):
            nextTransitions = [t for t in self.automaton[state] if not self.isWasteState(t[0])]
            if state in self.endingState:
                nextRand = random.randint(0, len(nextTransitions))
                
                if nextRand == len(nextTransitions):
                    return res[:-1]
                else:
                    state = nextTransitions[nextRand][0]
                    res += nextTransitions[nextRand][1] + " "
            else:
                nextRand = random.randint(0, len(nextTransitions) -1)
                state = nextTransitions[nextRand][0]
                res += nextTransitions[nextRand][1] + " "
        
        return res
                
    def getTransitionList(self):
        return [(s,e,t) for s,trans in self.automaton.iteritems() for e,t in trans]
    
    @staticmethod
    def importFromFile(filePath):
        f=open(filePath)
        lines = [line.strip() for line in f.readlines()]
        automate = Automate()
        for line in lines:
            lineSplit = line.split('\t')
            
            if len(lineSplit) == 1:
                automate.setStateFinal(lineSplit[0])
            elif len(lineSplit) == 4:
                (stateInit, stateEnd, inputData, trans) = lineSplit
                
                if stateInit not in automate.automaton:
                    automate.addState(stateInit)
                    
                if stateEnd not in automate.automaton:
                    automate.addState(stateEnd)
            
                automate.addTransition(stateInit, stateEnd, trans)
            else:
                print "Error :", filePath, lineSplit
            
        automate.setStateInitial('0')
            
        return automate
        
    def __str__(self):
        
        s = "States : " + ', '.join(self.automaton.keys()) + '\n'
        s += "Initial states : " + ', '.join(self.startingStates) + "\n"
        s += "Ending states : " + ', '.join(self.endingState) + "\n\n"
        for (k,v) in self.automaton.iteritems():
            for (e, t) in v:
                s += str(k) + " -- " + str(t) + " --> " + str(e) + "\n"

        return s
    
    def __repr__(self):
        return self.__str__()
        
    def generateExamples(self, nbExample):
        res = []
        
        while len(res) < nbExample:
            example = self.generate()
            
            if example not in res:
                res.append(example)
                
        return res
        
    def isConsistent(self, listExample):
        listTransition = self.getTransitionList()
        transitionUnchecked = self.getTransitionList()
        
        i = 0
        while len(listTransition) != 0 and i < len(listExample):
            splitExample = listExample[i].split(" ")
            assert(len(self.startingStates) == 1)
            state = self.startingStates[0]
            
            for ex in splitExample:
                trans = [(s,e,t) for (s,e,t) in listTransition if s==state and t == tuple(ex.split('.'))]
                assert(len(trans) == 1)
                
                if trans[0] in transitionUnchecked:
                    transitionUnchecked.remove(trans[0])
                state = trans[0][1]
                
            assert(state in self.endingState)
            i += 1
            
        return len(transitionUnchecked) == 0
        
    def accept(self, example):
        listTransition = self.getTransitionList()
        splitExample = example.split(" ")
        
        assert(len(self.startingStates) == 1)
        
        state = self.startingStates[0]

        for ex in splitExample:
            trans = [(s,e,t) for (s,e,t) in listTransition if s==state and t == ex]
            if len(trans) > 1:
                print trans
            if len(trans) == 0:
                return False
            else:
                assert(len(trans) == 1)
            
                state = trans[0][1]
                
                
        return state in self.endingState
        
    def probaOnState(self, state):
        if state in self.startingStates:
            probaInit = 1/len(self.startingStates)
        else:
            probaInit = 0
            
        
        
    
    
def loadAllAutomaton():
    listAutomate = {}
    for f in listdir('DataAutomate/'):
        if isfile(join('DataAutomate/', f)):
            listAutomate[join('DataAutomate/', f)] = Automate.importFromFile(join('DataAutomate/', f))
            
    return listAutomate