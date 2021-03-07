
from Symbol import Symbol

#* The tape of a Turing machine
#  has a potentially infinite ist of symbols
#  only the so far accessed portion is stored
class Tape:
    # has a list storing the used portion and a blank symbol on the rest of it 
    def __init__(self, blank: Symbol) -> None:
        self.blank = blank
        self.tape = list()
        self.offset = 0
    
    # erases all input on the tape
    def erase(self):
        self.tape = list()
        self.offset = 0

    # inputs a new word onto the tape
    def newInput(self, word: list[Symbol]) -> None:
        self.erase()
        self.tape = word.copy()
        self.offset = 0
    
    # returns the used portion of the tape
    def asList(self) -> list[Symbol]:
        return self.tape
    
    # writes a symbol to a specified position of the tape
    def write(self, pos: int, symbol: Symbol) -> None:
        index = self.offset + pos

        if index >= len(self.tape):
            self.tape.extend([self.blank] * (index - len(self.tape)))
        elif index < 0:
            self.tape = ([self.blank] * (-index)) + self.tape
            self.offset -= index
        
        self.tape[self.offset + pos] = symbol

    # reads a symbol off the tape
    def read(self, pos: int) -> Symbol:
        index = self.offset + pos
        return self.tape[index] if 0 <= index < len(self.tape) else self.blank