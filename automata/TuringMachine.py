from __future__ import annotations
from automata.Automaton import Automaton
from enum import IntEnum
from typing import Any

from automata.Symbol import Symbol
from automata.Tape import Tape

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
        self.dict = {}
        for state, stateDict in trans.items():
            fillGeneric: TransRet | None = None
            for symbol, retVal in stateDict.items():
                if symbol.isGeneric:
                    fillGeneric = retVal
                else:
                    self.dict[(state, symbol)] = retVal
            
            if fillGeneric is not None:
                for symbol in alphabet:
                    if (state, symbol) not in self.dict:
                        if fillGeneric[1].isGeneric:
                            self.dict[(state, symbol)] \
                                = (fillGeneric[0], symbol, fillGeneric[2])
                        else:
                            self.dict[(state, symbol)] = fillGeneric
    
    def __call__(self, state: State, symbol: Symbol) -> TransRet:
        return self.dict[(state, symbol)]

class TuringMachineID:
    def __init__(self, tm: TuringMachine) -> None:
        self.head = tm.head
        self.state = tm.state
        self.tape = tm.tape.copy()

#* a Turing machine with a single bidirectional tape and head
class TuringMachine(Automaton):
    #! TODO: assert proper set inclusions
    def __init__(self,
                 states: set[State],
                 tapeAlphabet: set[Symbol],
                 blank: Symbol,
                 inputAlphabet: set[Symbol],
                 startingState: State,
                 finalStates: set[State],
                 transition: TransFunc | TransDict
                 ) -> None:
        self.states = states.copy()
        self.tapeAlphabet = tapeAlphabet.copy()
        self.blank = blank
        self.inputAlphabet = inputAlphabet.copy()
        self.startingState = startingState
        self.finalStates = finalStates.copy()
        if isinstance(transition, dict):
            self.transFunc = TransFunc(transition, tapeAlphabet)
        else:
            self.transFunc = transition

        self.tape = Tape(blank)
        self.head = 0
        self.state = startingState

    def read(self) -> Symbol:
        return self.tape.read(self.head)

    def write(self, symbol: Symbol) -> None:
        self.tape[self.head] = symbol

    def reset(self) -> None:
        self.tape.clear()
        self.head = 0
        self.state = self.startingState

    def step(self) -> None:
        nextState, nextSymbol, dir = self.transFunc(self.state, self.read())
        self.write(nextSymbol)
        self.head += dir
        self.state = nextState

    def __call__(self,
                 input: list[Symbol] | None = None,
                 logFile: str | None = None,
                 ) -> list[Symbol]:
        if input is not None:
            self.reset()
            self.tape.input(input)

        if logFile is not None:
            idList: list[TuringMachineID] = []
            idList.append(TuringMachineID(self))

            while self.state not in self.finalStates:
                self.step()
                idList.append(TuringMachineID(self))
            
            with open(logFile, "w") as f:
                for id in idList:
                    f.write(str(id))
        else:
            while self.state not in self.finalStates:
                self.step()

        retVal: list[Symbol] = []
        while self.read() != self.blank:
            retVal.append(self.read())
            self.head += 1
        
        return retVal

    def __str__(self) -> str:
        return f"{self.tape}\n{self.state: >self.head+3}\n"
         