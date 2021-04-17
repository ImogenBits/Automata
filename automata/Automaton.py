from __future__ import annotations
from typing import Generic, TypeVar, Any
from automata.Tape import Storage
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

    def __call__(self, input: InType) -> RetType:
        return self.dict[input]


class Log:
    pass

class Automaton(Generic[InType, RetType]):
    FuncType = TransFunc[InType, RetType]
    LogType = Log
    StorageType = Storage

    def __init__(self,
                 transFunc: TransFunc[InType, RetType]
                          | dict[InType, RetType],
                 alphabet: Alphabet,
                 ) -> None:
        self.alphabet = alphabet
        if isinstance(transFunc, TransFunc):
            self.transFunc = transFunc
        else:
            self.transFunc = self.FuncType(transFunc, alphabet)
        
        self.storage = self.StorageType()
