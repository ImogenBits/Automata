from __future__ import annotations
from typing import Generic, Sequence, TypeVar, Any

import sys
print(sys.executable)

from PIL.Image import Image
from PIL.Image import new as newImage
from PIL.ImageDraw import ImageDraw
from automata.Tape import BoundedTape
from automata.Symbol import Symbol, Alphabet, SymbolIter

def anyGeneric(input: Symbol | tuple[Any, ...]) -> bool:
    if isinstance(input, Symbol):
        return input.isGeneric
    for s in input:
        if isinstance(s, Symbol) and s.isGeneric:
            return True
    return False

class ID:
    def __init__(self, aut: Automaton[Any, Any, Any, Any]) -> None:
        self.lBound, self.rBound = aut.tape.bounds()
        self.tape = aut.tape.copy()

    def bounds(self) -> tuple[int, int]:
        return self.lBound, self.rBound

    def __len__(self) -> int:
        return self.rBound - self.lBound
    
    def createImage(self, scale: int, imStart: int, imEnd: int) -> Image:
        image = newImage("RGB", (scale * (imEnd - imStart), scale), "#000000")
        imDraw = ImageDraw(image)
        for j, symbol in enumerate(self.tape[imStart:imEnd]):
            x = scale * j
            imDraw.rectangle([x, 0, x + scale, scale],
                            fill = symbol.color)
        return image



IDT = TypeVar("IDT", bound=ID)

class Log(Generic[IDT]):
    def __init__(self,
                 auto: Automaton[Any, Any, IDT, Any],
                 scale: int = 10,
                 width: int | None = 200,
                 steps: int | None = 100) -> None:
        self.auto = auto
        self.scale = scale
        self.width = width
        self.steps = steps
        self.arr: list[IDT] = []
    
    def log(self) -> None:
        self.arr.append(self.auto.getID())

    def createImage(self) -> Image:
        steps, width, scale = self.steps, self.width, self.scale
        if steps is None:
            steps = len(self.arr)
        arr = self.arr[:steps]

        if width is None:
            width = 0
            for t in arr:
                width = max(width, len(t))
                
        lBound, rBound = 0, 0
        for t in arr:
            l, r = t.bounds()
            lBound = min(lBound, l)
            rBound = max(rBound, r)
        
        if rBound - lBound <= width:
            imStart = lBound - ((width - (rBound - lBound)) // 2)
        else:
            imStart = -((width - len(arr[0])) // 2)
        imEnd = imStart + width

        buffer = 3 * scale
        imWidth = scale * width + 2 * buffer
        imHeight = scale * steps + 2 * buffer

        image = newImage("RGB", (imWidth, imHeight), "#000000")
        for i, id in enumerate(arr):
            idIm = id.createImage(scale, imStart, imEnd)
            image.paste(idIm, (buffer, buffer + i * scale))
        
        self.image = image
        return image


InT = TypeVar("InT", Symbol, tuple[Any, ...])
RetT = TypeVar("RetT", Symbol, tuple[Any, ...])

class TransFunc(Generic[InT, RetT]):
    def __init__(self,
                 transDict: dict[InT, RetT],
                 alphabet: Alphabet
                 ) -> None:
        self.dict: dict[InT, RetT]
        self.dict = {}

        genericRules: list[tuple[InT, RetT]] = []
        for input, output in transDict.items():
            if anyGeneric(input):
                genericRules.append((input, output))
            else:
                self.dict[input] = output
        
        for genIn, genOut in genericRules:
            for input, output in SymbolIter(genIn, genOut, alphabet):
                if input not in self.dict:
                    self.dict[input] = output

    def __call__(self, input: InT) -> RetT:
        return self.dict[input]


ResultT = TypeVar("ResultT")
LogT = TypeVar("LogT", bound=Log[Any])

class Automaton(Generic[InT, RetT, IDT, ResultT]):
    FuncT = TransFunc[InT, RetT]
    LogT = Log[IDT]
    TapeT = BoundedTape

    def __init__(self,
                 transFunc: TransFunc[InT, RetT]
                          | dict[InT, RetT],
                 alphabet: Alphabet,
                 ) -> None:
        self.alphabet = alphabet
        if isinstance(transFunc, TransFunc):
            self.transFunc = transFunc
        else:
            self.transFunc = self.FuncT(transFunc, alphabet)
        
        self.tape = self.TapeT()

    def reset(self):
        self.tape.clear()
    
    def getID(self) -> IDT:
        ...

    def step(self) -> bool:
        return False
    
    def run(self,
            input: Sequence[Symbol] | None = None,
            log: LogT[Any] | None = None,
            steps: int | None = None
           ) -> Any:
        self.reset()
        if input is not None:
            self.tape.input(input)
        
        if log is None:
            if steps is None:
                while not self.step():
                    pass
            else:
                i = 0
                while i < steps and not self.step():
                    pass
        else:
            if steps is None:
                log.log()
                while not self.step():
                    log.log()
                log.log()
            else:
                i = 0
                log.log()
                while i < steps and not self.step():
                    log.log()
                    i += 1
                log.log()
    
    def __call__(self,
                 input: Sequence[Symbol] | None = None,
                 log: Any | None = None,
                 steps: int | None = None
                ) -> Any:
        self.run(input, log, steps)
        
