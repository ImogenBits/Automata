from enum import Enum
from typing import Any, Callable

from Symbol import Symbol
from Tape import Tape

State = Any

class Direction(Enum):
    L = 1
    N = 2
    R = 3

#* a Turing machine with a single bidirectional tape and head
class TuringMachine:

    def __init__(self,
                 states: set[State],
                 tapeAlphabet: set[Symbol],
                 blankSymbol: Symbol,
                 inputAlphabet: set[Symbol],
                 startingState: State,
                 finalStates: set[State],
                 transitionFunc: Callable[[State, Symbol], tuple[State, Symbol, Direction]]
                 ) -> None:
        pass





    def deltaDictFunc(self, q, s):
        if s in self.deltaDict[q]:
            return self.deltaDict[q][s]
        elif X in self.deltaDict[q]:
            c, dir, qnew = self.deltaDict[q][X]
            return (s if c == X else c, dir, qnew)
        else:
            return (s, Dir.N, HLT)

    def cleanDict(self, d):
        res = dict()
        for state, trans in d.items():
            res[state] = dict()
            for s, tar in trans.items():
                cleanR = str(s)      if type(s)      == int else s
                cleanW = str(tar[0]) if type(tar[0]) == int else tar[0]
                res[state][cleanR] = (cleanW, tar[1], tar[2])
        return res

    def getState(self):
        if 0 <= self.tape.i <= len(self.tape.tape):
            #return " ".join([f"{s: <2}" for s in self.tape.tape[0:self.tape.i]] + [f"{self.q: <2}"] + [f"{s: <2}" for s in self.tape.tape[self.tape.i:]])
            l1 = "".join([f"{s: >3}" for s in self.tape.tape])
            l2 = "   " * self.tape.i + f"{self.q: >3}"
            return l1 + "\n" + l2 + "\n"
        else:
            return "index off of tape"

    def __init__(self, Q, G, b, S, q0, F, d):
        self.Q = Q.union({HLT})
        self.G = G
        self.b = b
        self.S = S
        self.q0 = q0
        self.F = F.union({HLT})
        if callable(d):
            self.d = d
        else:
            self.d = self.deltaDictFunc
            self.deltaDict = self.cleanDict(d)
        self.tape = Tape(G, b, S)
    
    def __call__(self, w, printStep = False, log = False):
        self.tape.input(w)
        self.q = self.q0
        file = None
        i = 0
        if log:
            file = open("log.txt", "w")
        while self.q not in self.F:
            if log:
                file.write(self.getState())
            if printStep:
                i += 1
                print(f"\r{i}", end="")
            c, dir, self.q = self.d(self.q, self.tape.read())
            self.tape.write(c)
            self.tape.move(dir)
        if log:
            file.write(self.getState())
        if printStep:
            i += 1
            print(f"\r{i}", end="")
        if log:
            file.close()
        if printStep:
            print("")
        out = ""
        r = self.tape.read()
        while r != self.tape.b:
            out += r
            self.tape.move(Dir.R)
            r = self.tape.read()
        return out