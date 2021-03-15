from __future__ import annotations
import itertools
from os import error

#* Symbols of some alphabet
#  currently only has a char c
#  should have a string that is a humna readable name (for indexing etc),
#  a char for internal representation (maybe),
#  and a colour for cellular automata (or just pretty TMs)
class Symbol:
    def __init__(self, c: str, isGeneric: bool = False):
        if len(c) > 3:
            raise error(f"Symbol needs to be a single char, not \"{c}\" with length {len(c)}")
        self.c = c
        self.isGeneric = isGeneric
        self.__name__ = c

    def __eq__(self, o: Symbol) -> bool:
        return self.c == o.c

    def __hash__(self) -> int:
        return self.c.__hash__()

    def __str__(self) -> str:
        return self.c
    
    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)
    
    @staticmethod
    def iterateGenerics(input: tuple[Symbol, ...], output: Symbol, alph: set[Symbol]) -> SymIter:
        return SymIter(input, output, alph)

class SymIter:
    def __init__(self, input: tuple[Symbol, ...], output: Symbol, alph: set[Symbol]) -> None:
        self.input = input
        self.output = output
        self.alph = alph

        self.indices: list[int] = list()
        for i in range(len(input)):
            if input[i].isGeneric:
                self.indices.append(i)
                if input[i] == output:
                    self.outIndex = i
        
        if self.outIndex is None and output.isGeneric:
            raise error(f"input tuple {input} does not contain output variable {output}")

        self.numVars = len(self.indices)
        self.vars = itertools.product(alph, repeat=self.numVars)

    def __iter__(self) -> SymIter:
        return self
    
    def __next__(self) -> tuple[tuple[Symbol, ...], Symbol]:
        varTuple = self.vars.__next__()
        resList = list(self.input)
        i = 0
        for indx in self.indices:
            resList[indx] = varTuple[i]
        
        if self.output.isGeneric:
            output = varTuple[self.outIndex]
        else:
            output = self.output
        
        return (tuple(resList), output)