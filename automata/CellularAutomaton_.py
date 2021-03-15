from __future__ import annotations
import itertools
import random
from typing import Optional
from os import error

from automata.Symbol_ import Symbol
from automata.Tape_ import Tape

Color = tuple[int, int, int]
RuleDict = dict[tuple[Symbol, ...], Symbol]
RuleNumber = int

def digitAt(num: int, pos: int, base: int = 10) -> int:
    return (num // (base ** pos)) % (base ** (pos + 1))

def anyGeneric(input: tuple[Symbol, ...]) -> bool:
    for s in input:
        if s.isGeneric:
            return True
    return False


class RuleFunc:
    def __init__(self,
                 rule: RuleDict | RuleNumber,
                 neighborhoood: int,
                 alphabet: set[Symbol] | list[Symbol]
                 ) -> None:
        self.dict: RuleDict = {}
        if isinstance(rule, RuleNumber) and isinstance(alphabet, list):
            i = 0
            len = len(alphabet)
            for comb in itertools.product(alphabet, repeat=neighborhoood):
                self.dict[comb] = alphabet[digitAt(rule, i, len)]
                i += 1
        elif isinstance(rule, dict) and isinstance(alphabet, set):
            for input, output in rule.items():
                if anyGeneric(input):
                    for tup, out in Symbol.iterateGenerics(input, output, alphabet):
                        self.dict[tup] = out
                else:
                    self.dict[input] = output
        else:
            raise error(f"""Created a RuleFunc with RuleNumber {rule}
                            but the alphabet was a set""")
    
    def __call__(self, input: tuple[Symbol, ...]) -> Symbol:
        return self.dict[input]

class CellularAutomaton:
    def __init__(self,
                 rule: RuleFunc | RuleDict | RuleNumber,
                 neighborhood: int = 3,
                 alphabet: set[Symbol] = {Symbol("0"), Symbol("1")},
                 blankSymbol: Symbol = Symbol("0")
                 ) -> None:
        self.neighborhood = neighborhood
        self.alphabet = alphabet.copy()
        alphSize = len(self.alphabet)
        self.maximumRuleNumber = alphSize ** (alphSize ** self.neighborhood)

        if isinstance(rule, RuleFunc):
            self.ruleFunc = rule
        else:
            self.ruleFunc = RuleFunc(rule, neighborhood, alphabet)

        self.tape = Tape(blankSymbol)
    
    def reset(self):
        self.tape.clear()

    def step(self):
        left, right = self.tape.bounds()
        newList: list[Symbol] = []
        for i in range(left, right):
            pass

    def __call__(self,
                 input: Optional[list[Symbol]] = None,
                 randInputlength: Optional[int] = None):
        self.reset()
        if input is not None:
            self.tape.input(input)
        elif input is None and randInputlength:
            alphList = list(self.alphabet)
            self.tape.input([random.choice(alphList) for _ in range(randInputlength)])
        else:
            raise error("provide either input or randInputLength")

        

        
