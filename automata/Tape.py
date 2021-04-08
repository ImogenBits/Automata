from __future__ import annotations
from math import ceil
from typing import Sequence
from automata.Symbol import Symbol

def getEdge(a: int, step: int) -> int:
    return a + (step - (a % step))

#* The tape of a Turing machine
#  has a potentially infinite ist of symbols
#  only the so far accessed portion is stored
class Tape(Sequence[Symbol]):
    # has a list storing the used portion and a blank symbol on the rest of it 
    def __init__(self,
                 blankSymbol: Symbol,
                 word: Sequence[Symbol] | None = None
                 ) -> None:
        self.blank = blankSymbol
        self.__right: list[Symbol] = list()
        self.__left: list[Symbol] = list()
        if word is not None:
            self.input(word)

    # erases all input on the tape
    def clear(self):
        self.__right = list()
        self.__left = list()

    # inputs a new word onto the tape
    def input(self, word: Sequence[Symbol], offset: int = 0) -> None:
        self.clear()
        for i, s in enumerate(word):
            self[i + offset] = s
    
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

    def copy(self,
             start: int | None = None,
             stop: int | None = None,
             step: int = 1,
             offset: int = 0,
             moveToStart: bool = False
             ) -> Tape:
        
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

            if moveToStart:
                tar = 0
            else:
                tar = -1 * ceil((min(stop, 0) - firstElem) / step)
                tar = min(tar, 0)

            currElem = firstElem
            while currElem < stop:
                tape[tar] = self.read(currElem)
                currElem += step
                tar += 1
            return tape

        else:
            step *= -1
            firstElem = start - (start % step) + offset
            if start % step < offset:
                firstElem -= step

            if moveToStart:
                tar = 0
            else:
                tar = -1 * ceil((firstElem - max(stop, 0)) / step)
                tar = min(tar, 0)

            currElem = firstElem
            while currElem > stop:
                tape[tar] = self.read(currElem)
                currElem -= step
                tar += 1
            return tape

    def __getitem__(self,
                    key: int | slice | tuple[slice, int],
                   ) -> Symbol | Tape:
        if isinstance(key, int):
            return self.read(key)
        elif isinstance(key, slice):
            return self.copy(key.start, key.stop, key.step)
        else:
            slc = key[0]
            return self.copy(slc.start, slc.stop, slc.step, key[1])

    def bounds(self) -> tuple[int, int]:
        return -1 * len(self.__left), len(self.__right) - 1

    def __iter__(self) -> Tape:
        self.__iterLeft = True
        self.__iterObj = reversed(self.__left)
        return self
    
    def __next__(self) -> Symbol:
        try:
            return next(self.__iterObj)
        except StopIteration:
            if self.__iterLeft:
                self.__iterLeft = False
                self.__iterObj = iter(self.__right)
                return next(self.__iterObj)
            else:
                del self.__iterObj
                del self.__iterLeft
                raise StopIteration()
    
    def __len__(self) -> int:
        return len(self.__left) + len(self.__right)

    def toStrList(self) -> list[str]:
        l = [str(c) for c in self.__left[::-1]]
        r = [str(c) for c in self.__right[1:]]
        return l + [f"|{self[0]}|"] + r

    def __str__(self) -> str:
        return "".join(self.toStrList())
    
    def __repr__(self) -> str:
        return f"""[{", ".join(self.toStrList())}]"""
    
    def trim(self) -> Tape:
        for l in [self.__left, self.__right]:
            while len(l) != 0 and l[-1] == self.blank:
                l.pop()
        return self

    def __add__(self, x: Tape) -> Tape:
        newTape = self.copy()
        _, tar = newTape.bounds()
        for sym in x:
            newTape.write(tar, sym)
            tar += 1
        return newTape