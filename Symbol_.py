from os import error


#* Symbols of some alphabet
#  currently only has a char c
#  should have a string that is a humna readable name (for indexing etc),
#  a char for internal representation (maybe),
#  and a colour for cellular automata (or just pretty TMs)
class Symbol:
    def __init__(self, c: str):
        if len(c) != 1:
            raise error(f"Symbol needs to be a single char, not \"{c}\" with length {len(c)}")
        self.c = c



