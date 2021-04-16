from __future__ import annotations
from typing import Sequence, Any
from automata.Symbol import Symbol



class Storage(Sequence[Symbol]):
    def __init__(self, word: Sequence[Symbol] | None = None) -> None:
        if word is not None:
            self.input(word)
    
    def clear(self):
        ...
    
    def input(self, word: Sequence[Symbol], offset: int = 0) -> None:
        ...
    
    def read(self, pos: int) -> Symbol:
        ...

    def copy(self,
             start: int | None = None,
             stop: int | None = None,
             step: int = 1,
             offset: int = 0,
             moveToStart: bool = False
             ) -> Storage:
        ...
    
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
    
    def __iter__(self) -> Storage:
        ...
    
    def __next__(self) -> Symbol:
        ...
    
    def __len__(self) -> int:
        ...

    def toStrList(self) -> list[str]:
        ...
    
    def __str__(self) -> str:
        return "".join(self.toStrList())
        
    def __repr__(self) -> str:
        return f"""[{", ".join(self.toStrList())}]"""
    
    def __add__(self, x: Any) -> Storage:
        ...