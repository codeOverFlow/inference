#coding:utf-8
from Classe_Automate import *
from Utils2 import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

mot_vide="_"

class L_star:
    def __init__(self, alphabet, oracle):
        self.alphabet = alphabet
        self.oracle = oracle
        self.table = {'red' : {mot_vide : {mot_vide : self.oracle.query(mot_vide)}}, 
            'blue' : {a : {mot_vide : self.oracle.query(a)} for a in self.alphabet}}
        self.column = [mot_vide]
        #pp.pprint(self.table)
        
    def concatWord(self, a, b):
        if a==mot_vide:
            return b
        elif b==mot_vide:
            return a
        else:
            return a+' '+b
            
    def addEntry(self, table, line, column):
        ex = self.concatWord(line, column)
        
        find = False
        for t in ['red', 'blue']:
            for l,w in self.table[t].iteritems():
                for c,v in w.iteritems():
                    if v != None and self.concatWord(l,c) == ex:
                        self.table[table][line][column] = v
                        find = True
                        break
                if find:
                    break
            if find:
                break
            
        if not find:
            self.table[table][line][column] = self.oracle.query(ex)
        
    def addRed(self, example):
        if example not in self.table['red']:
            self.table['red'][example] = {}
            for column in self.column:
                self.addEntry('red', example, column)
        
        if example in self.table['blue']:
            del self.table['blue'][example]
            
        for a in self.alphabet:
            newEx = self.concatWord(example, a)
            if newEx not in self.table['red'] and newEx not in self.table['blue']:
                self.table['blue'][newEx] = {}
                for column in self.column:
                    self.addEntry('blue', newEx, column)
            
    def addExperiment(self, example):
        #For a better method : verify other column than mot_vide
        if example not in self.column:
            self.column.append(example)
            for t in ['red', 'blue']:
                for line, v in self.table[t].iteritems():
                    self.addEntry(t, line, example)
                
        
        
    def isComplete(self):
        for t in ['red', 'blue']:
            for line,e in self.table[t].iteritems():
                for column in self.column:
                    if column not in e or e[column] == None:
                        return (t,line,column)
        return None
        
    def makeComplete(self, tuple_ex):
        t = tuple_ex[0]
        line = tuple_ex[1]
        column = tuple_ex[2]
        self.table[t][line][column] = self.oracle.query(self.concatWord(line, column))
        
        
    def makeConsistent(self, letter):
        self.addExperiment(letter)
            
    def isConsistent(self):
        counterExample = None
        for l,v in self.table['red'].iteritems():
            for ll,vv in self.table['red'].iteritems():
                if l == ll:
                    continue
                if v == vv:
                    for a in self.alphabet:
                        nl = self.concatWord(l,a)
                        nll = self.concatWord(ll,a)
                        
                        if nl in self.table['red'].keys():
                            if nll in self.table['red'].keys():
                                for exp, v1 in self.table['red'][nl].iteritems():
                                    if v1 != self.table['red'][nll][exp]:
                                        counterExample = self.concatWord(a, exp)
                                        break
                            elif nll in self.table['blue'].keys():
                                for exp, v1 in self.table['red'][nl].iteritems():
                                    if v1 != self.table['blue'][nll][exp]:
                                        counterExample = self.concatWord(a, exp)
                                        break
                        elif nl in self.table['blue'].keys():
                            if nll in self.table['red'].keys():
                                for exp, v1 in self.table['blue'][nl].iteritems():
                                    if v1 != self.table['red'][nll][exp]:
                                        counterExample = self.concatWord(a, exp)
                                        break
                            elif nll in self.table['blue'].keys():
                                for exp, v1 in self.table['blue'][nl].iteritems():
                                    if v1 != self.table['blue'][nll][exp]:
                                        counterExample = self.concatWord(a, exp)
                                        break
                        
                        if counterExample:
                            break
                if counterExample:
                    break
            if counterExample:
                break
        return counterExample
        
    
    def makeClosed(self, key):
        self.table['red'][key] = self.table['blue'][key]
        del self.table['blue'][key]
        for a in self.alphabet:
            newKey = self.concatWord(key, a)
            if newKey not in self.table['blue']:
                self.table['blue'][newKey] = {}
                for column in self.column:
                    self.addEntry('blue',newKey,column)
        
        
    def isClosed(self):
        save = None
        for l,v in self.table['blue'].iteritems():
            save = l
            for ll,vv in self.table['red'].iteritems():
                if v == vv:
                    save = None
                    break
            if save != None:
                break
        return save
    
        
    def generateAutomaton(self):
        automaton = Automate()
        done={tuple([b for a,b in self.table['red'][mot_vide].iteritems()]) : mot_vide}
        automaton.addState(mot_vide, isStarting=True, isFinal=self.table['red'][mot_vide][mot_vide])
        for s,v in self.table['red'].iteritems():
            line = tuple([b for a,b in v.iteritems()])
            if line not in done:
                automaton.addState(s, isStarting=False, isFinal=v[mot_vide])
                done[line] = s
            if s != mot_vide:
                splitT = s.split(' ')
                line = tuple([b for a,b in v.iteritems()])
                
                if len(splitT) == 1:
                    automaton.addTransition(mot_vide, done[line], s)
                else:
                    previousT = ' '.join(splitT[:-1])
                    assert(previousT in self.table['blue'] or previousT in self.table['red'])
                    if previousT in self.table['red']:
                        previousLine = tuple([b for a,b in self.table['red'][previousT].iteritems()])
                        if previousLine not in done:
                            automaton.addState(previousT, isStarting=False, isFinal=self.table['red'][previousT][mot_vide])
                            done[previousLine] = previousT
                    
                    else:
                        previousLine = tuple([b for a,b in self.table['blue'][previousT].iteritems()])
                        if previousLine not in done:
                            automaton.addState(previousT, isStarting=False, isFinal=self.table['blue'][previousT][mot_vide])
                            done[previousLine] = previousT
                    
                    
                    automaton.addTransition(done[previousLine], done[line], splitT[-1])
        
        for t,v in self.table['blue'].iteritems():
            splitT = t.split(' ')
            line = tuple([b for a,b in v.iteritems()])
            if len(splitT) == 1:
                if (mot_vide, done[line], t) not in automaton.getTransitionList():
                    automaton.addTransition(mot_vide, done[line], t)
            else:
                previousT = ' '.join(splitT[:-1])
                assert(previousT in self.table['blue'] or previousT in self.table['red'])
                if previousT in self.table['red']:
                    previousLine = tuple([b for a,b in self.table['red'][previousT].iteritems()])
                else:
                    previousLine = tuple([b for a,b in self.table['blue'][previousT].iteritems()])
                if (done[previousLine], done[line], splitT[-1]) not in automaton.getTransitionList():
                    automaton.addTransition(done[previousLine], done[line], splitT[-1])
        
        return automaton
        
        
    def run(self):
        a=(False,[])
        count={"Pos":0, "Neg":0}
        while not a[0]:
            comp = self.isComplete()
            #print "Complete :", str(comp)
            cons = self.isConsistent()
            #print "Consistent :", str(cons)
            clos = self.isClosed()
            #print "Close :", str(clos) + "\n\n"
            while comp != None or cons != None or clos != None:
                if comp != None:
                    self.makeComplete(comp)
                if cons != None:
                    self.makeConsistent(cons)
                if clos != None:
                    self.makeClosed(clos)
                comp = self.isComplete()
                #print str(comp)
                cons = self.isConsistent()
                #print str(cons)
                clos = self.isClosed()
                #print str(clos) + '\n\n'
            
            pp.pprint(self.table)
            
            print self.generateAutomaton(), "\n"
        
            a=self.oracle.equivalence(self.generateAutomaton())
            
            if not a[0]:
                print "Ex", a[1]
                assert(a[1] not in self.table['red'] and a[1] not in self.table['blue'])
                
                if self.oracle.query(a[1]
                
                splitEx = a[1].split(' ')
                for i in range(0, len(splitEx)):
                    self.addRed(' '.join(splitEx[0:i+1]))
            
            print True
            #print self.generateAutomaton()
            
    def run_without_equivalence(self):
        a=(False,[])
        while not a[0]:
            comp = self.isComplete()
            #print "Complete :", str(comp)
            cons = self.isConsistent()
            #print "Consistent :", str(cons)
            clos = self.isClosed()
            #print "Close :", str(clos) + "\n\n"
            while comp != None or cons != None or clos != None:
                if comp != None:
                    self.makeComplete(comp)
                if cons != None:
                    self.makeConsistent(cons)
                if clos != None:
                    self.makeClosed(clos)
                comp = self.isComplete()
                #print str(comp)
                cons = self.isConsistent()
                #print str(cons)
                clos = self.isClosed()
                #print str(clos) + '\n\n'
            
            #pp.pprint(self.table)
            
            #print self.generateAutomaton(), "\n"
        
            l_automaton = self.generateAutomaton()
            a=(True, None)
            
            if len(l_automaton.endingState) == 0:
                ex = self.oracle.automaton.generate()
                while len(ex.split(' ')) > 10:
                    ex = self.oracle.automaton.generate()
                    
                a=(False, ex)
            else:
                for i in range(50):
                    ex = l_automaton.generate()
                    while len(ex.split(' ')) > 10:
                        ex = l_automaton.generate()
                        
                    if not self.oracle.query(ex):
                        a=(False, ex)
                        break
                
                for i in range(50):
                    ex = self.oracle.automaton.generate()
                    while len(ex.split(' ')) > 10:
                        ex = self.oracle.automaton.generate()
                        
                    if not l_automaton.accept(ex):
                        a=(False, ex)
                        break
                
                
            if not a[0]:
                #print "Ex", a[1]
                assert(a[1] not in self.table['red'] and a[1] not in self.table['blue'])
                splitEx = a[1].split(' ')
                for i in range(0, len(splitEx)):
                    self.addRed(' '.join(splitEx[0:i+1]))
        print self.oracle.equivalence(self.generateAutomaton())
            
        #print self.generateAutomaton()
        
        
class Oracle:
    def __init__(self, automaton):
        self.automaton = automaton
        
    def query(self, example):
        return self.automaton.accept(example)
        
    def equivalence(self, l_automaton):
        #print self.automaton, l_automaton
        #print distanceEuclidean(self.automaton, l_automaton)
        #return testEquivalence(self.automaton, l_automaton)
        e=Equivalence(self.automaton, l_automaton)
        return e.test()

class ManuelOracle:
    def query(self, example):
        print
        print "Query :", example
        if raw_input() == "y":
            return True
        else:
            return False
    
    def equivalence(self, l_automaton):
        print
        print "Equivalence :"
        print l_automaton
        
        i = raw_input()
        if i == "None":
            return True, None
        else:
            return False, i

if __name__ == '__main__':        
    #automate = Automate.importFromFile("DataAutomate/141_Cambodian.fsa.att")
    automate = Automate.importFromFile("automateTest.fsa.att")
    
    print "A trouver :"
    print automate
    print "\n"
    
    #oracle = ManuelOracle() 
    oracle = Oracle(automate)
    alphabet = automate.getAlphabet()
    l_star = L_star(alphabet, oracle)
    
    l_star.run()
    #l_star.run_without_equivalence()
    
    #pp.pprint(l_star.table)
            
    #print l_star.generateAutomaton(), "\n"
    
def test_cours():
    l_star = L_star(None, None)
    l_star.alphabet = ['a', 'b']
    l_star.column = ['', 'a']
    
    l_star.table = {'red' : {'' : {'' : True, 'a' : True},
                            'b' : {'' : True, 'a' : True},
                            'b a' : {'' : True, 'a' : False},
                            'b a a' : {'' : False, 'a' : False}},
                    'blue' : {'a' : {'' : True, 'a' : False},
                                'b b' : {'' : True, 'a' : True},
                                'b a b' : {'' : True, 'a' : True},
                                'b a a a' : {'' : False, 'a' : False},
                                'b a a b' : {'' : True, 'a' : False}}}
                                
    pp.pprint(l_star.table)
                                
    
    print l_star.generateAutomaton()