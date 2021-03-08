from enum import Enum
from typing import Any, Union

from Symbol_ import Symbol
from Tape_ import Tape

State = Any

class Direction(Enum):
    L = 1
    N = 2
    R = 3

TransRet = tuple[State, Symbol, Direction]
TransDict = dict[State, dict[Symbol, TransRet]]

class TransFunc():
    def __init__(self, trans: TransDict):
        self.dict: dict[tuple[State, Symbol], TransRet]
        self.dict = dict()
    

#* a Turing machine with a single bidirectional tape and head
class TuringMachine:
    #! TODO: assert proper set inclusions
    def __init__(self,
                 states: set[State],
                 tapeAlphabet: set[Symbol],
                 blankSymbol: Symbol,
                 inputAlphabet: set[Symbol],
                 startingState: State,
                 finalStates: set[State],
                 transition: Union[TransFunc, TransDict]
                 ) -> None:
        self.states = states.copy()
        self.tapeAlphabet = tapeAlphabet.copy()
        self.blankSymbol = blankSymbol
        self.inputAlphabet = inputAlphabet.copy()
        self.startingState = startingState
        self.finalStates = finalStates.copy()
        if isinstance(transition, dict):
            self.transFunc = TransFunc(transition)
        else:
            self.transFunc = transition

        self.tape = Tape(blankSymbol)
        self.head = 0




