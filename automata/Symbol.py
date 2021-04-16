from __future__ import annotations
import itertools
from os import error, replace
from typing import Generic, Iterable, Iterator, TypeVar, Any

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


def replace(tar: Symbol | tuple[Any, ...], gen: Symbol, rep: Symbol) -> Any:
    if isinstance(tar, Symbol):
        return replace((tar,), gen, rep)[0]
    else:
        ret = list(tar)
        for i, s in enumerate(ret):
            if isinstance(s, Symbol) and s == gen:
                ret[i] = rep
        return tuple(ret)

InType = TypeVar("InType", Symbol, tuple[Any, ...])
RetType = TypeVar("RetType", Symbol, tuple[Any, ...])
class SymbolIter(Generic[InType, RetType]):
    """
    iterates over all possible replacements of generic symbols
    with ones from the alphabet
    """
    def __init__(self, input: InType, output: RetType, alph: Alphabet) -> None:
        self.input = input
        self.output = output
        self.alph = alph
        self.varList: list[Symbol] = []

        varCount = 0
        if isinstance(input, tuple):
            for i in range(len(input)):
                if (isinstance(input[i], Symbol)
                        and input[i].isGeneric
                        and input[i] not in self.varList):
                    varCount += 1
                    self.varList.append(input[i])
        else:
            if input.isGeneric:
                varCount = 1
                self.varList.append(input)
            else:
                varCount = 0
        self.__iterObj = itertools.product(alph, repeat=varCount)


    def __iter__(self) -> SymbolIter[InType, RetType]:
        return self
    
    def __next__(self) -> tuple[InType, RetType]:
        rep = next(self.__iterObj)
        retIn: Any = self.input
        retOut: Any = self.output
        for i, sym in enumerate(rep):
            retIn = replace(retIn, self.varList[i], sym)
            retOut = replace(retOut, self.varList[i], sym)

        return retIn, retOut



class Alphabet(frozenset[Symbol]):
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

#* Overloaded functions from frozenset
 
    def __iter__(self) -> Iterator[Symbol]:
        return iter(self.__list)

    def union(self, *s: Iterable[Symbol]) -> Alphabet:
        retAlph = self
        for alph in s:
            retAlph =  retAlph | Alphabet(alph)
        return retAlph

    def __or__(self, s: Alphabet) -> Alphabet:
        retAlph = set(s)
        for sym in s:
            retAlph.add(sym)
        return Alphabet(retAlph)

    def intersection(self, *others: Iterable[object]) -> Alphabet:
        retAlph = self
        for other in others:
            newSet: set[Symbol] = {s for s in other if isinstance(s, Symbol)}
            retAlph = retAlph & Alphabet(newSet)
        return retAlph
    
    def __and__(self, s: Alphabet) -> Alphabet:
        retAlph: set[Symbol] = set()
        for sym in s:
            if sym in self:
                retAlph.add(sym)
        for sym in self:
            if sym in s:
                retAlph.add(sym)
        return Alphabet(retAlph)

    def difference(self, *s: Iterable[object]) -> Alphabet:
        retAlph = self
        for a in s:
            newSet: set[Symbol] = {s for s in a if isinstance(s, Symbol)}
            retAlph = retAlph - Alphabet(newSet)
        return retAlph
    
    def __sub__(self, s: Alphabet) -> Alphabet:
        retAlph = set(s)
        for sym in s:
            retAlph.discard(sym)
        return Alphabet(retAlph)

    def symmetric_difference(self, s: Iterable[Symbol]) -> Alphabet:
        return self ^ Alphabet(s)
    
    def __xor__(self, s: Alphabet) -> Alphabet:
        return (self | s) - (self & s)

    def copy(self) -> Alphabet:
        return Alphabet(self.__list)