from __future__ import annotations
from math import ceil
from typing import Callable
from automata.Symbol import Symbol

def getEdge(a: int, step: int) -> int:
    return a + (step - (a % step))

#* The tape of a Turing machine
#  has a potentially infinite ist of symbols
#  only the so far accessed portion is stored
class Tape:
    # has a list storing the used portion and a blank symbol on the rest of it 
    def __init__(self, blankSymbol: Symbol) -> None:
        self.blank = blankSymbol
        self.__right: list[Symbol] = list()
        self.__left: list[Symbol] = list()

    # erases all input on the tape
    def clear(self):
        self.__right = list()
        self.__left = list()

    # inputs a new word onto the tape
    def input(self, word: list[Symbol], offset: int = 0) -> None:
        self.clear()
        for i, s in enumerate(word):
            self[i + offset] = s
        
        #self.__left.clear()
        #self.__right = word.copy()
    
    # returns the used portion of the tape
    def copy(self) -> Tape:
        n = Tape(self.blank)
        n.__right = self.__right.copy()
        n.__left = self.__left.copy()
        return n
    
    # writes a symbol to a specified position of the tape
    def write(self, pos: int, symbol: Symbol) -> None:
        if pos >= 0:
            arr = self.__right
        else:
            arr = self.__left
            pos = -(1 + pos)
        
        if pos >= len(arr):
            arr.extend([self.blank] * (pos - len(arr) + 1))
        arr[pos] = symbol
        
    def __setitem__(self, pos: int, symbol: Symbol) -> None:
        return self.write(pos, symbol)

    # reads a symbol off the tape
    def read(self, pos: int) -> Symbol:
        if pos >= 0:
            arr = self.__right
        else:
            arr = self.__left
            pos = -(1 + pos)
        
        if pos >= len(arr):
            return self.blank
        else:
            return arr[pos]
        
    def __getitem__(self,
                    key: int | slice | tuple[slice, int],
                   ) -> Symbol | Tape:
        if isinstance(key, int):
            return self.read(key)

        if isinstance(key, tuple):
            offset = key[1]
            key = key[0]
        else:
            offset = 0
        start, stop, step = key.start, key.stop, key.step
        
        step = 1 if step is None else step
        if start is None:
            if step > 0:
                start = -1 * len(self.__left)
            else:
                start = len(self.__right) - 1
        if stop is None:
            if step > 0:
                stop = len(self.__right)
            else:
                stop = -1 * len(self.__left) - 1

        tape = Tape(self.blank)
        if (step > 0 and start >= stop) or (step < 0 and start <= stop):
            return tape

        if step > 0:
            firstElem = start - (start % step) + offset
            if start % step > offset:
                firstElem += step
            endLeft = stop if stop < 0 else 0
            tar = -1 * ceil((endLeft - firstElem) / step)

            currElem = firstElem
            while currElem < stop:
                tape[tar] = self.read(currElem)
                currElem += step
                tar += 1
            return tape

        else:
            step *= -1
            firstElem = start - (start % step) + offset
            if start % step > offset:
                firstElem -= step
            endRight = stop if stop > 0 else 0
            tar = -1 * ceil(-(endRight - firstElem) / step)

            currElem = firstElem
            while currElem > stop:
                tape[tar] = self.read(currElem)
                currElem -= step
                tar += 1
            return tape

    def bounds(self) -> tuple[int, int]:
        return len(self.__left), len(self.__right)

    def __iter__(self) -> Tape:
        self.__iterLeft = True
        self.__iter = reversed(self.__left)
        return self
    
    def __next__(self) -> Symbol:
        try:
            return next(self.__iter)
        except StopIteration:
            if hasattr(self, "__iterLeft"):
                del self.__iterLeft
                self.__iter = iter(self.__right)
                return next(self.__iter)
            else:
                del self.__iter
                raise StopIteration()
    
    def __len__(self) -> int:
        return len(self.__left) + len(self.__right)

    def __str__(self) -> str:
        return "".join([f"{s: >3}" for s in self])
    
    def __repr__(self) -> str:
        return str(self.__left[::-1])[:-1] + f", |{self[0]}|, " + str(self.__right[1:])[1:]