from __future__ import annotations
from typing import Generic, TypeVar, Any
from automata.Tape import Tape
from automata.Symbol import Symbol, Alphabet

class TransFunc:
    def __init__(self,
                 rule: dict[Any, Any],
                 alphabet: Alphabet
                 ) -> None:
        pass

class Automaton:
    def __init__(self,
                 alphabet: Alphabet,
                 transFunc: TransFunc | dict[Any, Any]
                 ) -> None:
        self.alphabet = alphabet
        if isinstance(transFunc, TransFunc):
            self.transFunc = 