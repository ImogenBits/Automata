from os import error
from __future__ import annotations

#* Symbols of some alphabet
#  currently only has a char c
#  should have a string that is a humna readable name (for indexing etc),
#  a char for internal representation (maybe),
#  and a colour for cellular automata (or just pretty TMs)
class Symbol:
    def __init__(self, c: str, isGeneric: bool = False):
        if len(c) != 1:
            raise error(f"Symbol needs to be a single char, not \"{c}\" with length {len(c)}")
        self.c = c
        self.isGeneric = isGeneric

    def __eq__(self, o: Symbol) -> bool:
        return self.c == o.c

