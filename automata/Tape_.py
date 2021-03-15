from automata.Symbol_ import Symbol

#* The tape of a Turing machine
#  has a potentially infinite ist of symbols
#  only the so far accessed portion is stored
class Tape:
    # has a list storing the used portion and a blank symbol on the rest of it 
    def __init__(self, blankSymbol: Symbol) -> None:
        self.blank = blankSymbol
        self.arr: list[Symbol] = list()
        self.offset = 0

    # erases all input on the tape
    def clear(self):
        self.arr = list()
        self.offset = 0

    # inputs a new word onto the tape
    def input(self, word: list[Symbol]) -> None:
        self.clear()
        self.arr = word.copy()
        self.offset = 0
    
    # returns the used portion of the tape
    def asList(self) -> list[Symbol]:
        return self.arr
    
    # writes a symbol to a specified position of the tape
    def write(self, pos: int, symbol: Symbol) -> None:
        index = self.offset + pos

        if index >= len(self.arr):
            self.arr.extend([self.blank] * (index - len(self.arr) + 1))
        elif index < 0:
            self.arr = ([self.blank] * (-index)) + self.arr
            self.offset -= index
        
        self.arr[self.offset + pos] = symbol

    # reads a symbol off the tape
    def read(self, pos: int) -> Symbol:
        index = self.offset + pos
        return self.arr[index] if 0 <= index < len(self.arr) else self.blank

    def bounds(self) -> tuple[int, int]:
        return (self.offset, self.offset + len(self.arr))