from __future__ import annotations
import itertools
import random
from typing import Sequence
from collections import deque
from os import error

from automata.Symbol import Alphabet, Symbol
from automata.Tape import Tape
from automata.Automaton import Automaton, TransFunc, Log, ID

RuleDict = dict[tuple[Symbol, ...], Symbol]

def digitAt(num: int, pos: int, base: int = 10) -> int:
    return (num // (base ** pos)) % base

class CAID(ID):
    pass

class CALog(Log[CAID]):
    pass

class CARuleFunc(TransFunc[tuple[Symbol, ...], Symbol]):
    def __init__(self,
                 rule: RuleDict | int,
                 neighborhoood: int,
                 alphabet: Alphabet
                ) -> None:
        
        if isinstance(rule, int):
            ruleDict: RuleDict = {}
            i = 0
            l = len(alphabet)
            for comb in itertools.product(alphabet, repeat=neighborhoood):
                ruleDict[comb] = alphabet[digitAt(rule, i, l)]
                i += 1
        else:
            ruleDict = rule

        super().__init__(ruleDict, alphabet)



class CellularAutomaton(Automaton[tuple[Symbol, ...], Symbol, CAID, Tape]):
    FuncT = CARuleFunc
    LogT = CALog
    TapeT = Tape

    def __init__(self,
                 rule: CARuleFunc | RuleDict | int,
                 neighborhood: int = 3,
                 alphabet: Alphabet = Alphabet([Symbol("0"), Symbol("1")]),
                 blank: Symbol = Symbol("0")
                 ) -> None:
        self.neighborhood = neighborhood
        self.blank = blank

        if isinstance(rule, CARuleFunc):
            self.ruleFunc = rule
        else:
            self.ruleFunc = CARuleFunc(rule, neighborhood, alphabet)

        self.tape = Tape(blank)

    def getID(self) -> CAID:
        return CAID(self)

    def step(self) -> bool:
        hasChanged = False
        tape = self.tape
        neighborhood = self.neighborhood
        left, right = tape.bounds()
        buffer = deque([self.blank] * neighborhood, maxlen = neighborhood)
        cOff = self.neighborhood // 2
        for i in range(left - neighborhood + 1, right + 1):
            buffer.append(tape.read(i + neighborhood - 1))
            newSymbol = self.ruleFunc(tuple(buffer))
            if tape.read(i + cOff) != newSymbol:
                hasChanged = True
                tape.write(i + cOff, newSymbol)
                pass
        return not hasChanged

    def __call__(self,
                 input: Sequence[Symbol] | None = None,
                 log: CALog | None = None,
                 steps: int | None = None,
                 randInputlength: int | None = None,
                 ) -> Tape:
        self.reset()

        if input is None and randInputlength is not None:
            alphList = list(self.alphabet)
            input = [random.choice(alphList) for _ in range(randInputlength)]
        
        if input is None:
            raise error("provide either input or randInputLength")

        self.run(input, log, steps)

        return self.tape.copy()

