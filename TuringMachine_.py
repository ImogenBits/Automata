from enum import IntEnum
from typing import Any, Optional, Union

from Symbol_ import Symbol
from Tape_ import Tape

State = Any

class Direction(IntEnum):
    L = -1
    N = 0
    R = 1



TransRet = tuple[State, Symbol, Direction]
TransDict = dict[State, dict[Symbol, TransRet]]

class TransFunc():
    def __init__(self, trans: TransDict, alphabet: set[Symbol]) -> None:
        self.dict: dict[tuple[State, Symbol], TransRet]
        self.dict = dict()

        for state, stateDict in trans.items():
            fillGeneric: Optional[TransRet] = None
            for symbol, retVal in stateDict.items():
                if symbol.isGeneric:
                    fillGeneric = retVal
                else:
                    self.dict[(state, symbol)] = retVal
            
            if fillGeneric is not None:
                for symbol in alphabet:
                    if (state, symbol) not in stateDict:
                        if fillGeneric[1].isGeneric:
                            self.dict[(state, symbol)] \
                                = (fillGeneric[0], symbol, fillGeneric[2])
                        else:
                            self.dict[(state, symbol)] = fillGeneric
    
    def __call__(self, state: State, symbol: Symbol) -> TransRet:
        return self.dict[(state, symbol)]

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
            self.transFunc = TransFunc(transition, tapeAlphabet)
        else:
            self.transFunc = transition

        self.tape = Tape(blankSymbol)
        self.head = 0
        self.state = startingState

    def reset(self) -> None:
        self.tape.clear()
        self.head = 0
        self.state = self.startingState

    def step(self) -> None:
        nextState, nextSymbol, dir = \
            self.transFunc(self.state, self.tape.read(self.head))
        self.tape.write(self.head, nextSymbol)
        self.head += dir
        self.state = nextState

    def __call__(self,
                 input: Optional[list[Symbol]] = None,
                 logFile: Optional[str] = None,
                 ) -> list[Symbol]:
        if input is not None:
            self.reset()
            self.tape.input(input)
        
        if logFile is not None:
            idList: list[list[Symbol]] = []
            idList.append(self.tape.asList())
            
            while self.state not in self.finalStates:
                self.step()
                idList.append(self.tape.asList())
            
            with open(logFile, "w") as f:
                for id in idList:
                    L1 = "".join({f"{s.c: >3}" for s in id})
                    L2 = "   " * self.head + f"{self.state: >3}"
                    f.write(L1 + "\n" + L2 + "\n")
        else:
            while self.state not in self.finalStates:
                self.step()
        
        retVal: list[Symbol] = []
        while self.tape.read(self.head) != self.blankSymbol:
            retVal.append(self.tape.read(self.head))
            self.head += 1
        
        return retVal