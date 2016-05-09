from Classe_Automate import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Equivalence:
    def __init__(self, automate1, automate2):
        self.classe = {}
        self.automate1 = automate1
        self.automate2 = automate2
        
        self.automate1.addState('NONE')
        for k,v in self.automate1.automaton.iteritems():
            for a in self.automate1.getAlphabet():
                if a not in [t for (s,t) in v]:
                    self.automate1.addTransition(k, 'NONE', a)
        self.automate2.addState('NONE')
        for k,v in self.automate2.automaton.iteritems():
            for a in self.automate2.getAlphabet():
                if a not in [t for (s,t) in v]:
                    self.automate2.addTransition(k, 'NONE', a)
        
        assert(set(self.automate1.getAlphabet()) == set(self.automate2.getAlphabet()))
        
        self.alphabet = self.automate1.getAlphabet()
        
        for s in automate1.automaton.keys(): 
            self.classe["1_"+s] = "1_"+s
        for s in automate2.automaton.keys():
            self.classe["2_"+s] = "2_"+s
    
    def test(self):
        if not self.automate1.startingStates:
            return False
        if not self.automate2.startingStates:
            return False
        
        return self.state_equi("1_"+self.automate1.startingStates[0], "2_"+self.automate2.startingStates[0], "")

    def state_equi(self, s1, s2, path):
        res = (True, None)
        if s1[2:] in self.automate1.endingState and s2[2:] not in self.automate2.endingState or s1[2:] not in self.automate1.endingState and s2[2:] in self.automate2.endingState:
            return (False, path)
        else:
            if self.classe[s1] != self.classe[s2]:
                saves1 = self.classe[s1]
                if self.classe[s2] not in self.classe[s1]:
                    self.classe[s1] = self.classe[s1] + ' ' + self.classe[s2]
                if self.classe[s1] not in self.classe[s2]:
                    self.classe[s2] = saves1 + ' ' + self.classe[s2]
                for a in self.alphabet:
                    t1 = [t for t in self.automate1.automaton[s1[2:]] if t[1] == a]
                    assert(len(t1) == 1 or len(t1)==0)
                    t2 = [t for t in self.automate2.automaton[s2[2:]] if t[1] == a]
                    assert(len(t2) == 1 or len(t2)==0)
                    if len(t1) != len(t2):
                        return (False, path)
                    if len(t1) == 1:
                        nextPath = a if path == "" else path+' '+a
                        equiNext = self.state_equi("1_"+t1[0][0], "2_"+t2[0][0],nextPath)
                        if not equiNext[0]:
                            return equiNext
            return res
            
if __name__ == '__main__':
    automate = Automate()
    automate.addState('5', True, False)
    automate.addState('6', False, False)
    automate.addState('4', False, False)
    automate.addState('7', False, True)
    automate.addTransition('5','6', 'a')
    automate.addTransition('5','6', 'b')
    automate.addTransition('6','7', 'a')
    automate.addTransition('6','4', 'b')
    automate.addTransition('7','7', 'a')
    automate.addTransition('7','7', 'b')
    
    print automate
    
    automate2 = Automate()
    automate2.addState('5', True, False)
    automate2.addState('6', False, False)
    automate2.addState('7', False, True)
    automate2.addTransition('5','6', 'a')
    automate2.addTransition('5','6', 'b')
    automate2.addTransition('6','7', 'a')
    automate2.addTransition('6','6', 'b')
    automate2.addTransition('7','7', 'a')
    automate2.addTransition('7','7', 'b')
    
    print '############################\n', automate2
    
    eq = Equivalence(automate, automate2)
    print eq.test()