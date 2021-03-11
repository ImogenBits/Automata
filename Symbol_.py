from __future__ import annotations
from os import error

#* Symbols of some alphabet
#  currently only has a char c
#  should have a string that is a humna readable name (for indexing etc),
#  a char for internal representation (maybe),
#  and a colour for cellular automata (or just pretty TMs)
class Symbol:
    def __init__(self, c: str, isGeneric: bool = False):
        if len(c) > 3:
            raise error(f"Symbol needs to be a single char, not \"{c}\" with length {len(c)}")
        self.c = c
        self.isGeneric = isGeneric
        self.__name__ = c

    def __eq__(self, o: Symbol) -> bool:
        return self.c == o.c

    def __hash__(self) -> int:
        return self.c.__hash__()

    def __str__(self) -> str:
        return self.c
    
    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)