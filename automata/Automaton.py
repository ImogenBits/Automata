from __future__ import annotations
from typing import Generic, TypeVar, Any
from automata.Tape import Tape
from automata.Symbol import Symbol, Alphabet, SymbolIter

def anyGeneric(input: Symbol | tuple[Any, ...]) -> bool:
    if isinstance(input, Symbol):
        return input.isGeneric
    for s in input:
        if isinstance(s, Symbol) and s.isGeneric:
            return True
    return False

InType = TypeVar("InType", Symbol, tuple[Any, ...])
RetType = TypeVar("RetType", Symbol, tuple[Any, ...])

class TransFunc(Generic[InType, RetType]):
    def __init__(self,
                 transDict: dict[InType, RetType],
                 alphabet: Alphabet
                 ) -> None:
        self.dict: dict[InType, RetType]
        self.dict = {}

        genericRules: list[tuple[InType, RetType]] = []
        for input, output in transDict.items():
            if anyGeneric(input):
                genericRules.append((input, output))
            else:
                self.dict[input] = output
        
        for genIn, genOut in genericRules:
            for input, output in SymbolIter(genIn, genOut, alphabet):
                if input not in self.dict:
                    self.dict[input] = output



class Automaton(Generic[InType, RetType]):
    def __init__(self,
                 alphabet: Alphabet,
                 transFunc: TransFunc[InType, RetType] | dict[InType, RetType]
                 ) -> None:
        self.alphabet = alphabet
        if isinstance(transFunc, TransFunc):
            self.transFunc = transFunc
        else:
            self.transFunc = TransFunc


class Log(Generic[InType, RetType]):
    pass