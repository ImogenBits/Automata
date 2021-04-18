from __future__ import annotations
from math import ceil
from typing import Iterator, Sequence, Any
from automata.Symbol import Symbol

END_SYMBOL = Symbol("__END__")

class BoundedTape(Sequence[Symbol]):
    def __init__(self, word: Sequence[Symbol] | None = None) -> None:
        self.__arr: list[Symbol] = []
        if word is not None:
            self.input(word) 

    def clear(self) -> None:
        self.__arr = []

    def input(self, word: Sequence[Symbol]) -> None:
        self.__arr = [END_SYMBOL] * (len(word) + 1)
        for i, s in enumerate(word):
            self.__arr[i] = s
            
    def write(self, pos: int, symbol: Symbol) -> None:
        self.__arr[pos] = symbol
        
    def __setitem__(self, pos: int, symbol: Symbol) -> None:
        return self.write(pos, symbol)

    def read(self, pos: int) -> Symbol:
        return self.__arr[pos]

    def copy(self,
             start: int | None = None,
             stop: int | None = None,
             step: int = 1,
             ) -> BoundedTape:
        return BoundedTape(self.__arr[start:stop:step])

    def __getitem__(self,
                    s: int | slice,
                   ) -> Any:
        if isinstance(s, int):
            return self.read(s)
        else:
            return self.copy(s.start, s.stop, s.step)
    
    def bounds(self) -> tuple[int, int]:
        return 0, len(self.__arr) - 1
    
    def __iter__(self) -> Iterator[Symbol]:
        return iter(self.__arr)

    def __len__(self) -> int:
        return len(self.__arr)
    
    def toStrList(self) -> list[str]:
        return [str(c) for c in self.__arr]
    
    def __str__(self) -> str:
        return "".join(self.toStrList())
        
    def __repr__(self) -> str:
        return f"""[{", ".join(self.toStrList())}]"""

    def __add__(self, x: Any) -> BoundedTape:
        return BoundedTape(self.__arr[:-1] + [c for c in x])


def getEdge(a: int, step: int) -> int:
    return a + (step - (a % step))

#* The tape of a Turing machine
#  has a potentially infinite ist of symbols
#  only the so far accessed portion is stored
class Tape(BoundedTape):
    # has a list storing the used portion and a blank symbol on the rest of it 
    def __init__(self,
                 blankSymbol: Symbol,
                 word: Sequence[Symbol] | None = None
                 ) -> None:
        self.blank = blankSymbol
        self.__right: list[Symbol] = []
        self.__left: list[Symbol] = []
        if word is not None:
            self.input(word)

    # erases all input on the tape
    def clear(self):
        self.__right = []
        self.__left = []

    # inputs a new word onto the tape
    def input(self, word: Sequence[Symbol], offset: int = 0) -> None:
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
                    s: int | slice | tuple[slice, int],
                   ) -> Any:
        if isinstance(s, int):
            return self.read(s)
        elif isinstance(s, slice):
            return self.copy(s.start, s.stop, s.step)
        else:
            slc = s[0]
            return self.copy(slc.start, slc.stop, slc.step, s[1])

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