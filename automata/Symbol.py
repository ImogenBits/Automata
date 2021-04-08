from __future__ import annotations
import itertools
from os import error
from typing import Iterable, Iterator

class Symbol:
    """
    The symbols automata read.
    Symbols are identified by the attribute c, which is 3 or fewer chars long.
    When rendered in a CA color will be displayed instead of c.
    Generic Symbols are used as variables in transition functions.
    """
    def __init__(self,
                 c: str,
                 color: tuple[int, int, int] | None = (0, 0, 0),
                 isGeneric: bool = False,
                 ) -> None:
        if len(c) > 3:
            raise error(f"Symbol needs to be 3 chars or shorter, not \"{c}\" with length {len(c)}")
        self.c = c
        self.isGeneric = isGeneric
        self.__name__ = c
        self.color = color

    def __eq__(self, o: Symbol) -> bool:
        return self.c == o.c

    def __hash__(self) -> int:
        return hash(self.c)
        
    def __str__(self) -> str:
        return self.c
    
    def __repr__(self) -> str:
        return self.c

    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)


class SymbolIter:
    """
    iterates over all possible replacements of generic symbols with ones from the alphabet
    """
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

    def __iter__(self) -> SymbolIter:
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


class Alphabet(set[Symbol]):
    """
    set of symbols that make up the words an automaton accepts
    """

    def __init__(self, iterable: Iterable[Symbol] | None = None) -> None:
        if iterable is not None:
            super().__init__(iterable)
            self.__list = list(iterable)
        else:
            super().__init__()
            self.__list: list[Symbol] = []
    
    def fillColors(self) -> None:
        pass

    def __getitem__(self, i: int) -> Symbol:
        return self.__list[i]

#* Overloaded functions from set
 
    def __iter__(self) -> Iterator[Symbol]:
        return iter(self.__list)

    def union(self, *s: Iterable[Symbol]) -> Alphabet:
        retAlph = self.copy()
        for alph in s:
            retAlph =  retAlph | Alphabet(alph)
        return retAlph

    def __or__(self, s: Alphabet) -> Alphabet:
        retAlph = self.copy()
        for sym in s:
            retAlph.add(sym)
        return retAlph

    def intersection(self, *s: Iterable[Symbol]) -> Alphabet:
        retAlph = self.copy()
        for alph in s:
            retAlph = retAlph & Alphabet(alph)
        return retAlph
    
    def __and__(self, s: Alphabet) -> Alphabet:
        retAlph = Alphabet()
        for sym in s:
            if sym in self:
                retAlph.add(sym)
        for sym in self:
            if sym in s:
                retAlph.add(sym)
        return retAlph

    def difference(self, *s: Iterable[Symbol]) -> Alphabet:
        retAlph = self.copy()
        for a in s:
            retAlph = retAlph - Alphabet(a)
        return retAlph
    
    def __sub__(self, s: Alphabet) -> Alphabet:
        retAlph = self.copy()
        for sym in s:
            retAlph.discard(sym)
        return retAlph

    def symmetric_difference(self, s: Iterable[Symbol]) -> Alphabet:
        return self ^ Alphabet(s)
    
    def __xor__(self, s: Alphabet) -> Alphabet:
        return (self | s) - (self & s)

    def copy(self) -> Alphabet:
        return Alphabet(self.__list)

    def update(self, *s: Iterable[Symbol]) -> None:
        for alph in s:
            self |= Alphabet(alph)
            
    def __ior__(self, s: Alphabet) -> Alphabet:
        for sym in s:
            self.add(sym)
        return self

    def intersection_update(self, *s: Iterable[Symbol]) -> None:
        for alph in s:
            self &= Alphabet(alph)

    def __iand__(self, s: Alphabet) -> Alphabet:
        for sym in self:
            if sym not in s:
                self.remove(sym)
        return self

    def difference_update(self, *s: Iterable[Symbol]) -> None:
        for alph in s:
            self -= Alphabet(alph)
        
    def __isub__(self, s: Alphabet) -> Alphabet:
        for sym in s:
            self.discard(sym)
        return self

    def symmetric_difference_update(self, s: Iterable[Symbol]) -> None:
        self ^= Alphabet(s)
    
    def __ixor__(self, s: Alphabet) -> Alphabet:
        for sym in s:
            if sym in self:
                self.remove(sym)
            else:
                self.add(sym)
        return self

    def add(self, element: Symbol) -> None:
        if element not in self:
            super().add(element)
            self.__list.append(element)
    
    def remove(self, element: Symbol) -> None:
        if element in self:
            super().remove(element)
            self.__list.remove(element)
        else:
            raise KeyError(element)

    def discard(self, element: Symbol) -> None:
        if element in self:
            self.remove(element)

    def pop(self) -> Symbol:
        elem = super().pop()
        self.__list.remove(elem)
        return elem
    
    def clear(self) -> None:
        super().clear()
        self.__list.clear()
